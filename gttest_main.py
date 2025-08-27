# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
작업자 행동 분석 시스템 메인 실행 파일 (원본 기반 v10.0)
- 세밀한 세그먼테이션으로 정확한 결과 생성
- Gemini API를 통한 정밀 행동 분류
- 사진과 같은 형태의 결과 출력
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# 분석 모듈 임포트
from gttest_analysis import WorkerAnalysisSystem

def setup_directories():
    """필요한 디렉토리 생성"""
    directories = ['results', 'logs', 'temp', 'robot_scripts']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

def validate_input_file(video_path):
    """입력 비디오 파일 검증"""
    if not os.path.exists(video_path):
        print(f"비디오 파일을 찾을 수 없습니다: {video_path}")
        return False
    
    supported_formats = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']
    file_ext = Path(video_path).suffix.lower()
    
    if file_ext not in supported_formats:
        print(f"지원되지 않는 파일 형식입니다: {file_ext}")
        print(f"지원되는 형식: {', '.join(supported_formats)}")
        return False
    
    return True

def display_welcome():
    """환영 메시지 표시"""
    print("=" * 80)
    print("작업자 행동 분석 → 로봇 제어 시스템 v10.0")
    print("=" * 80)
    print("세밀한 세그먼테이션을 통한 정밀 분석")
    print("12가지 작업 동작 인식:")
    print("  [2] Consult sheets | [3] Turn sheets | [4] Take screwdriver")
    print("  [5] Put down screwdriver | [6] Picking in front | [7] Picking left")
    print("  [8] Take measuring rod | [9] Put down measuring rod")
    print("  [10] Take subsystem | [11] Put down subsystem | [12] Assemble system")
    print("=" * 80)

def get_video_input():
    """비디오 파일 경로 입력"""
    print("\n비디오 파일 설정")
    print("-" * 40)
    
    # 기본 경로 확인
    default_paths = [
        '../video/r1test.mp4',
        './video/r1test.mp4', 
        'r1test.mp4'
    ]
    
    for default_path in default_paths:
        if os.path.exists(default_path):
            use_default = input(f"기본 비디오 파일을 사용하시겠습니까? [{default_path}] (y/n): ")
            if use_default.lower() in ['y', 'yes', '']:
                return default_path
            break
    
    # 사용자 입력
    while True:
        video_path = input("비디오 파일 경로를 입력하세요: ").strip().strip('"\'')
        if validate_input_file(video_path):
            return video_path
        
        retry = input("다시 시도하시겠습니까? (y/n): ")
        if retry.lower() not in ['y', 'yes']:
            return None

def analyze_video(analyzer):
    """비디오 분석 실행"""
    print("\n비디오 분석 시작")
    print("-" * 40)
    
    try:
        events = analyzer.analyze_video()
        
        if not events:
            print("분석 결과가 없습니다.")
            return None
        
        print(f"분석 완료: {len(events)}개 이벤트 감지")
        
        return {
            'events': events,
            'robot_selected_events': analyzer.select_robot_actions(events)
        }
        
    except Exception as e:
        print(f"분석 중 오류 발생: {e}")
        return None

def display_events_summary(events):
    """감지된 이벤트 요약 표시"""
    print("\n감지된 작업 이벤트 요약")
    print("=" * 80)
    
    # 이벤트 타입별 통계
    event_counts = {}
    total_duration = 0
    
    for event in events:
        event_type = event['type']
        duration = event.get('duration', 0)
        
        if event_type not in event_counts:
            event_counts[event_type] = {'count': 0, 'total_duration': 0}
        
        event_counts[event_type]['count'] += 1
        event_counts[event_type]['total_duration'] += duration
        total_duration += duration
    
    print(f"총 이벤트 수: {len(events)}개")
    print(f"총 분석 시간: {total_duration:.1f}초")
    print("\n동작별 통계:")
    print("-" * 60)
    print(f"{'동작 타입':<20} {'횟수':<8} {'총 시간':<10}")
    print("-" * 60)
    
    for event_type, stats in sorted(event_counts.items()):
        print(f"{event_type:<20} {stats['count']:<8} {stats['total_duration']:<8.1f}")
    
    print("-" * 60)

def display_detailed_events(events):
    """상세 이벤트 목록 표시 - 사진과 같은 형태 (시간 출력)"""
    print("\n상세 이벤트 목록 (Meta-Action Label 형태)")
    print("=" * 65)
    
    # 이벤트 타입을 번호로 변환
    type_to_number = {
        "consult_sheets": 2,
        "turn_sheets": 3, 
        "take_screwdriver": 4,
        "put_down_screwdriver": 5,
        "picking_in_front": 6,
        "picking_left": 7,
        "take_measuring_rod": 8,
        "put_down_measuring_rod": 9,
        "take_subsystem": 10,
        "put_down_subsystem": 11,
        "assemble_system": 12,
        "meta_action": 1
    }
    
    # 사진과 같은 형태로 출력 (시간으로)
    print("Meta-Action Label".ljust(25) + "Start Time (s)".rjust(15) + "End Time (s)".rjust(15))
    print("-" * 65)
    
    for event in events:
        event_type = event['type']
        number = type_to_number.get(event_type, 1)
        
        # 타입 이름을 사진과 같은 형태로 변환
        display_names = {
            "consult_sheets": "Consult sheets",
            "turn_sheets": "Turn sheets",
            "take_screwdriver": "Take screwdriver", 
            "put_down_screwdriver": "Put down screwdriver",
            "picking_in_front": "Picking in front",
            "picking_left": "Picking left",
            "take_measuring_rod": "Take measuring rod",
            "put_down_measuring_rod": "Put down measuring rod",
            "take_subsystem": "Take subsystem",
            "put_down_subsystem": "Put down subsystem", 
            "assemble_system": "Assemble system",
            "meta_action": "Meta action"
        }
        
        display_name = display_names.get(event_type, event_type)
        label = f"[{number}] {display_name}"
        
        start_time = event.get('start_time', 0)
        end_time = event.get('end_time', 0)
        
        print(f"{label:<25} {start_time:>14.2f} {end_time:>14.2f}")
    
    print("-" * 65)
    print(f"총 {len(events)}개 이벤트")

def save_analysis_results(analysis_data, video_path):
    """분석 결과 저장"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"results/{Path(video_path).stem}_{timestamp}.json"
    
    try:
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, ensure_ascii=False, indent=4)
        print(f"분석 결과 저장 완료: {results_file}")
        return results_file
    except Exception as e:
        print(f"결과 저장 실패: {e}")
        return None

def main():
    """메인 실행 함수"""
    setup_directories()
    display_welcome()
    
    # 비디오 파일 입력
    video_path = get_video_input()
    if not video_path:
        print("시스템을 종료합니다.")
        return False
        
    print(f"\n비디오 파일: {video_path}")

    # 분석 시스템 초기화
    try:
        print("분석 시스템 초기화 중...")
        analyzer = WorkerAnalysisSystem(video_path)
    except Exception as e:
        print(f"초기화 실패: {e}")
        return False

    # 비디오 분석 실행
    analysis_data = analyze_video(analyzer)
    if not analysis_data:
        print("비디오 분석에 실패했습니다.")
        return False
    
    events = analysis_data.get('events', [])
    if not events:
        print("분석 결과에 이벤트가 없습니다.")
        return False
        
    # 결과 표시
    display_events_summary(events)
    display_detailed_events(events)

    robot_events = analysis_data.get('robot_selected_events', [])
    robot_script_path = None
    
    if robot_events:
        print(f"\n로봇 제어 이벤트가 {len(robot_events)}개 감지되었습니다.")
        print("로봇 제어 스크립트 생성 중...")
        robot_script_path = analyzer.generate_robot_script(analysis_data)

    # 결과 저장
    results_file = save_analysis_results(analysis_data, video_path)
    
    # 최종 요약
    print("\n" + "=" * 80)
    print("분석 완료!")
    print("=" * 80)
    print(f"입력 비디오: {video_path}")
    print(f"감지된 이벤트: {len(events)}개")
    print(f"로봇 동작: {len(robot_events)}개")
    print(f"결과 파일: {results_file}")
    if robot_script_path:
        print(f"로봇 스크립트: {robot_script_path}")
    print("=" * 80)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

