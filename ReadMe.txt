자동매매 API            완료
백테스트 엔진           완료
멀티팩터 전략           완료
리스크 관리 실험        완료
동적 팩터 가중치        예정
시장 국면 인식          예정
실전 운용 시스템         진행 중

# Toss Trading Quant Project

Python 기반 해외주식 자동매매 및 퀀트 전략 연구 프로젝트

---

# 프로젝트 목표

1. 토스증권 Open API를 이용한 자동매매 시스템 구축
2. 다양한 퀀트 전략 구현 및 백테스트 엔진 개발
3. 팩터 기반 멀티팩터 로테이션 전략 연구
4. 리스크 관리 기법 및 동적 자산배분 연구
5. 실제 운용 가능한 프로토타입 구축

---

# 개발 환경

- Python 3.x
- Virtual Environment (.venv)
- Pandas
- Matplotlib
- Requests
- Toss Securities Open API

---

# 프로젝트 구조

```text
toss_trading/
│
├── auth/
│   └── token.py
│
├── api/
│   ├── overseas_stock.py
│   └── order.py
│
├── strategy/
│   ├── moving_average.py
│   ├── momentum.py
│   ├── rsi.py
│   ├── volatility_breakout.py
│   └── multifactor.py
│
├── backtest/
│   ├── engine.py
│   ├── multi_strategy.py
│   ├── rotation_engine.py
│   ├── multifactor_engine_v3.py
│   └── multifactor_engine_v4_1.py
│
├── visualization/
│   └── visualizer.py
│
├── main.py
├── main_rotation.py
├── main_multifactor.py
├── main_multifactor_v3.py
└── main_multifactor_v4_1.py
```

---

# 구현 완료 기능

## 1. 토스 API 연동

### 인증

- Access Token 발급
- 자동 갱신 구조 구현

### 시세 조회

- 국내 주식 일봉 조회
- 해외 주식 일봉 조회
- 캔들 데이터 DataFrame 변환

### 주문

- 시장가 매수
- 시장가 매도
- 주문 상태 조회
- 체결 여부 확인

---

## 2. 백테스트 엔진

구현 기능

- 자산 곡선(Equity Curve)
- 거래 내역 저장
- 총 수익률(Return)
- 최대 낙폭(MDD)
- 승률(Win Rate)
- 거래 횟수
- BUY / SELL 지점 시각화

---

# 구현한 전략

## Moving Average Cross

조건

```text
MA5 > MA20 → BUY
MA5 < MA20 → SELL
```

결과

```text
수익률 : 122.32%
MDD : -33.57%
승률 : 50%
```

특징

- 수익률 높음
- MDD 매우 큼
- 변동성 큼

---

## RSI Strategy

조건

```text
RSI 과매도 → BUY
RSI 과매수 → SELL
```

결과

```text
수익률 : 0%
```

특징

- 데이터 구간에서 신호 발생 거의 없음

---

## Volatility Breakout

특징

- 거래 빈도 높음
- 승률 높음
- 수익률 중간

---

## Momentum Strategy

특징

- 높은 수익률
- 비교적 낮은 MDD

결과

```text
수익률 : 192.85%
MDD : -23.99%
```

---

# Cross Sectional Momentum Rotation

Universe

```text
AMD
TSLA
AMZN
AAPL
SPXL
```

전략

1. 1개월
2. 3개월
3. 6개월

수익률을 계산

Composite Momentum Score 생성

매주 리밸런싱

Top1 종목에 100% 투자

결과

```text
수익률 : 50.33%
MDD : -44.62%
```

문제점

- MDD 매우 큼
- 단일 종목 집중

---

# AQR Style Multifactor Rotation

Universe

```text
AMD
TSLA
AMZN
AAPL
SPXL
QQQ
SOXX
SMH
NVDA
MSFT
META
GOOGL
AVGO
```

팩터

1. Momentum
2. Quality (ROE)
3. Value (PBR)
4. Volume

---

# Multifactor v3

구성

```text
Top2 Selection
Absolute Momentum Filter
MA Filter
RSI Filter
50:50 Allocation
Weekly Rebalancing
```

Base Weight

```text
Momentum : 40%
Quality : 25%
Value : 25%
Volume : 10%
```

결과

```text
수익률 : 76.01%
MDD : -15.72%
승률 : 66.67%
```

특징

- 현재까지 최고 성능
- 공격적 성향
- 반도체/AI 모멘텀 활용

---

# Multifactor v3 (Weight Tuning)

Weight

```text
Momentum : 50%
Quality : 30%
Value : 20%
Volume : 0%
```

결과

```text
수익률 : 54.00%
MDD : -15.19%
승률 : 60%
```

특징

- Volume Factor 제거
- 안정성 향상
- 수익률 감소

---

# Multifactor v4.1

추가 기능

```text
Inverse Volatility Position Sizing
```

예

```text
고변동 종목
↓
비중 축소

저변동 종목
↓
비중 확대
```

결과

```text
수익률 : 51.34%
MDD : -15.43%
승률 : 60%
```

결론

현재 Universe에서는

```text
Inverse Volatility
```

가 알파를 희석함.

고수익 종목

```text
AMD
SOXX
SMH
AVGO
```

의 비중이 감소하면서 성과가 악화됨.

---

# 실험을 통해 얻은 결론

## Momentum Factor

★★★★★

가장 설명력이 높음

---

## Quality Factor

★★★★☆

보조 팩터로 효과적

---

## Value Factor

★★★☆☆

중립적

---

## Volume Factor

★☆☆☆☆

현재 Universe에서는 효과 미미

---

## Inverse Volatility

★★☆☆☆

현재 Universe에서는 효과 제한적

---

# 현재 Best Model

## 공격형

```text
v3 Base

Momentum : 40%
Quality : 25%
Value : 25%
Volume : 10%

Return : 76.01%
MDD : -15.72%
```

---

## 보수형

```text
v3 Tuned

Momentum : 50%
Quality : 30%
Value : 20%
Volume : 0%

Return : 54.00%
MDD : -15.19%
```

---

# 다음 개발 계획

## v4.2

Dynamic Factor Weighting

예

상승장

```text
Momentum : 60%
Quality : 25%
Value : 15%
```

하락장

```text
Momentum : 30%
Quality : 40%
Value : 30%
```

---

## v4.3

Market Regime Filter

```text
QQQ > MA200
→ Risk On

QQQ < MA200
→ Risk Off
```

---

## 성과지표 추가

- Annual Return
- Annual Volatility
- Sharpe Ratio
- Sortino Ratio
- Calmar Ratio

---

# 최종 목표

실제 운용 가능한

AI + Multifactor + Dynamic Asset Allocation 기반

퀀트 자동매매 시스템 구축