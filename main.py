import os
import sys
import subprocess

# [경로 에러 완벽 차단] 현재 실행 폴더를 파이썬 경로 최상단에 배치
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

# 1. 구동 전 필요 패키지 무조건 자동 검출 및 설치 검사
REQUIRED_PACKAGES = ["numpy", "pandas", "matplotlib", "scipy", "openpyxl"]

def install_dependencies():
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package)
        except ImportError:
            print(f"[{package}] 라이브러리를 컴퓨터에서 찾을 수 없습니다. 자동으로 다운로드를 시도합니다...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            except Exception:
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", package])
                except Exception as e:
                    print(f"[{package}] 설치 과정 오류: {e}")
            print(f"[{package}] 설치 완료되었습니다!")

install_dependencies()

# 2. 패키지 로딩 완료 후 시스템 가동
import json
import config
from data.csv_generator import generate_mock_data
from simulator.optimizer import PolicyOptimizer
from visualization.graph import plot_optimization_history, plot_optimal_ratios

def main():
    print("=" * 60)
    print("    Starting Mobility Policy Simulator (Yangsan Area)")
    print("    [GA Multi-Variable Mode: 5 core policies optimal search]")
    print("=" * 60)
    
    # data 폴더 및 초기 테스트셋이 없을 경우 자동 주입 작동
    data_path = os.path.join(CURRENT_DIR, "data")
    if not os.path.exists(os.path.join(data_path, "traffic_hour.csv")):
        print("Initial dataset directory or CSV files not found. Creating mock dataset...")
        generate_mock_data(data_path)
        
    # 총 등록수 10000대 시뮬레이션 최적 가동 시작
    optimizer = PolicyOptimizer(total_vehicles=10000)
    best_policy, history = optimizer.run()
    
    # results 폴더 생성 및 저장
    results_path = os.path.join(CURRENT_DIR, "results")
    os.makedirs(results_path, exist_ok=True)
    
    with open(os.path.join(results_path, "optimal_policy_results.json"), "w", encoding="utf-8") as f:
        json.dump(best_policy, f, indent=4, ensure_ascii=False)
        
    print("\n[SUCCESS] 5개 변수 기반 유전 최적화 시뮬레이션 완료!")
    print("-" * 50)
    print("🎯 최적 차량 구성 비율:")
    for v_type, ratio in best_policy['ratios'].items():
        print(f"  - {v_type}: {ratio*100:.2f}%")
        
    print(f"🎯 최적 수소 지자체 지원비 ($x_4$): {best_policy['local_subsidy_h2']:,.0f} 원 / 대")
    print(f"🎯 신설 예정 수소 충전소 기수 ($x_5$): 추가 {best_policy['expanded_stations']} 개소")
    print("-" * 50)
    print("📊 종합 세부 평가 성능 지표:")
    metrics = best_policy['metrics']
    print(f"  - 예상 정부 지출 총합: {metrics['gov_spending']:,.0f} 원")
    print(f"  - 연간 이산화탄소 절감량: {metrics['co2_reduction_tons']:,.2f} Tons / Year")
    print(f"  - 충전 편의성 초과 지수: {metrics['infra_capacity_ratio']*100:.1f}%")
    print(f"  - 종합 최적합 평가 스코어: {best_policy['score']:.2f}")
    
    print("\n결과 데이터 세부 보고서 및 시각화 그래프 내보내기 진행 중...")
    # 변경: plot 함수들에 results_path를 전달
    plot_optimization_history(history, results_path)
    plot_optimal_ratios(best_policy['ratios'], results_path)
    print(f"내보내기 완료 -> 결과 확인 경로: {results_path}")
    print("=" * 60)

if __name__ == "__main__":
    main()
