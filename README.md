# Toss Trading Quant Project

Toss Securities Open API를 이용해 국내외 주식 데이터를 조회하고, 규칙 기반 전략과 멀티팩터 로테이션 전략을 연구하는 Python 프로젝트입니다. 장기적으로 paper trading과 live trading을 목표로 하지만, 현재 최우선 과제는 **재현 가능하고 편향을 통제한 연구용 백테스터**를 구축하는 것입니다.

기존 [ReadMe.txt](ReadMe.txt)는 초기 개발 과정과 당시 실험 결과를 담은 historical development note로 유지합니다. 그 문서의 수익률은 현재 코드 품질을 보증하는 결과가 아닙니다.

## 현재 개발 단계

현재 단계는 **exploratory prototype에서 reliable research backtester로 발전하는 과정**입니다.

- API 인증, 시세·candle·계좌·잔고 조회 코드가 있습니다.
- 시장가/지정가 주문 함수가 있으나 안전한 운영 계층은 아직 없습니다.
- 단일 종목 전략, 횡단면 모멘텀, 멀티팩터 백테스트가 구현되어 있습니다.
- 포트폴리오와 거래 기록의 기본 골격은 있으나 체결 시점, 거래비용, 통화, point-in-time 데이터와 리밸런싱 회계가 충분히 엄밀하지 않습니다.
- 따라서 현재 결과를 paper/live trading의 근거로 사용해서는 안 됩니다.

## 디렉터리 구조

```text
toss_trading/
├── api/
│   ├── auth.py                     # OAuth access token 발급
│   ├── market.py                   # 현재가 조회
│   ├── candle.py                   # 일봉 조회 및 DataFrame 변환
│   ├── account.py                  # 계좌 목록 조회
│   ├── balance.py                  # 보유 종목/잔고 조회
│   └── order.py                    # 매수, 매도, 주문 상태 및 체결 판정
├── backtest/
│   ├── engine.py                   # 단일 종목 signal backtest
│   ├── costs.py                    # commission/slippage 체결 비용 모델
│   ├── portfolio.py                # 공통 cash/position/P&L 원장
│   ├── accounting.py               # 목표비중 리밸런싱 및 결과 조립
│   ├── performance.py              # benchmark 및 표준 성과지표
│   ├── multi_strategy.py           # 네 가지 단일 종목 전략 비교
│   ├── rotation_engine.py          # 횡단면 모멘텀 로테이션
│   ├── multifactor_engine.py       # Multifactor v1
│   ├── multifactor_engine_v2.py
│   ├── multifactor_engine_v3.py
│   ├── multifactor_engine_v4.py
│   ├── multifactor_engine_v4_1.py
│   └── visualizer.py               # Equity curve 및 거래 지점 시각화
├── config/
│   └── settings.py                 # .env 환경변수 로드
├── data/
│   └── fundamental_data.py         # 현재는 수동 입력된 ROE/PBR
├── strategy/
│   ├── moving_average.py
│   ├── rsi.py
│   ├── volatility_breakout.py
│   ├── momentum.py
│   └── cross_sectional_momentum.py
├── main.py                         # 단일 종목 전략 비교
├── main_rotation.py                # 횡단면 모멘텀 백테스트
├── main_multifactor.py             # Multifactor v1
├── main_multifactor_v2.py
├── main_multifactor_v3.py
├── main_multifactor_v4.py
├── main_multifactor_v4_1.py
├── main_to_real_purchase           # 실제 주문 가능: 실행 금지
├── requirments.txt                 # 현재 파일명 오타 유지
├── ReadMe.txt                      # Historical development note
└── AGENTS.md                       # Repository 작업 및 안전 규칙
```

## API 모듈

| 모듈 | 역할 | 현재 주의점 |
|---|---|---|
| `api/auth.py` | client credentials 방식 access token 발급 | token cache/자동 갱신, timeout, 예외 처리가 없음 |
| `api/market.py` | 종목 현재가 조회 | `lastPrice`는 소수 문자열을 고려해 `float`로 변환함 |
| `api/candle.py` | 일봉 OHLCV 조회, 숫자·날짜 변환 및 정렬 | 응답 schema, null, timezone 검증이 부족함 |
| `api/account.py` | 계좌 목록 조회 | 응답 전체 출력으로 민감정보가 노출될 수 있음 |
| `api/balance.py` | 계좌 보유 종목 조회 | status/schema 검증과 반환 규약이 부족함 |
| `api/order.py` | 시장가/지정가 매수·매도, 주문 상태 조회 | 실제 주문 endpoint에 직접 연결되며 운영 안전장치가 부족함 |

API 응답의 `result`, `candles`, `lastPrice`, `status`, `execution` 필드는 항상 존재한다고 가정하면 안 됩니다. 가격·수량·통화·timestamp 단위를 명시적으로 검증해야 합니다.

## 구현된 전략

### Moving Average Cross

- 5일 이동평균이 20일 이동평균을 상향 돌파하면 매수 신호
- 5일 이동평균이 20일 이동평균을 하향 돌파하면 매도 신호

### RSI

- 14일 RSI가 30 미만이면 매수 신호
- RSI가 70 초과이면 매도 신호
- 현재 구현은 Wilder smoothing이 아닌 단순 rolling 평균을 사용합니다.

### Volatility Breakout

- 전일 고가-저가 범위와 당일 시가로 목표가격을 계산합니다.
- 당일 종가가 목표가격을 넘으면 매수 신호를 만들고 다음 날 매도 신호를 만듭니다.
- 현재는 실제 돌파가격이 아닌 당일 종가로 신호와 체결을 처리하므로 엄밀한 장중 돌파 모델이 아닙니다.

### Time-series Momentum

- 현재 종가의 20거래일 수익률이 양수이면 매수, 음수이면 매도합니다.

### Cross-sectional Momentum Rotation

- AMD, TSLA, AMZN, AAPL, SPXL을 현재 universe로 사용합니다.
- 21일, 63일, 126일 수익률의 가중합으로 종목별 score를 계산합니다.
- 5거래일 간격으로 Top 1 종목에 집중합니다.
- 모든 종목의 momentum이 음수여도 최고 score 종목을 보유하는 구조입니다.

### Multifactor Rotation

공통 팩터는 다음과 같습니다.

- Momentum: 일정 기간 가격 수익률
- Quality: 수동 입력된 ROE
- Value: 수동 입력된 PBR의 역순위
- Volume: 최근 평균 거래량과 이전 구간 평균 거래량의 변화

각 팩터를 universe 내 percentile rank로 변환하고 가중합 score를 만든 뒤 후보 중 상위 종목을 선택합니다.

## Multifactor 버전 차이

| 버전 | Universe/선택 | 필터 | 배분 및 추가 기능 |
|---|---|---|---|
| v1 | main 기준 5종목, Top 1 | 없음 | 가용 현금 기반 매수 |
| v2 | 13종목, Top 2 | 126일 절대 momentum, 장기 MA | 동일가중 목표 |
| v3 | 13종목, Top 2 | v2 + MA5 > MA20 + RSI > 55 | 동일가중 목표, main weight 50/30/20/0 |
| v4 | 13종목, Top 2 | v3 계열 필터 | ATR(20) × 3 trailing stop, main weight 네 팩터 각 25% |
| v4.1 | 13종목, Top 2 | v3 계열 필터 | 20일 inverse-volatility sizing, main weight 50/30/20/0 |

v4.1은 v4의 ATR stop을 포함하지 않으므로 v4에 기능을 순차 추가한 구조라기보다 v3에서 갈라진 실험에 가깝습니다. v2 이후도 과대 비중 포지션을 목표비중까지 줄이지 않고 탈락 종목 매도와 부족분 매수만 수행하므로 완전한 리밸런싱은 아닙니다.

## 백테스트 구조

### 단일 종목

```text
candle DataFrame
→ strategy가 buy_signal/sell_signal 생성
→ run_signal_backtest
→ 종가 기준 signal을 다음 거래일 시가에 체결
→ cash 및 단일 position 갱신
→ trades와 equity_curve 생성
→ total return, MDD, win rate 계산
```

### Rotation 및 Multifactor

```text
종목별 candle
→ 날짜 기준 close/volume DataFrame 정렬
→ lookback 이후 factor/score 계산
→ 일정 행 간격으로 리밸런싱
→ holdings dict와 cash 갱신
→ trades, rebalance_logs, equity_curve
→ total return, MDD, win rate
```

현재 MDD는 running peak 대비 하락률의 최솟값으로 계산합니다. Multifactor win rate는 여러 번 나누어 매수한 포지션의 평균 원가와 실현손익을 정확히 반영하지 않으므로 개선이 필요합니다.

모든 backtest engine은 공통 `ExecutionCostModel`과 `Portfolio`를 사용합니다. commission과 slippage의 기본값은 기존 동작과의 호환을 위해 0입니다. 목표비중 리밸런싱은 비중 초과 포지션도 매도하며, 평균 원가에는 매수 commission이 포함됩니다. 매도 거래의 `realized_pnl`은 평균 원가, 매도 commission 및 slippage가 반영된 값입니다.

각 결과에는 `cash`, `positions`, `realized_pnl`, `unrealized_pnl`, `total_commission`, `total_slippage_cost`와 `performance`가 포함됩니다. `performance`는 total return, CAGR, annual volatility, MDD, Sharpe, Sortino, Calmar, turnover를 제공하며, 엔진의 `benchmark` 인수에 날짜 인덱스를 가진 가격 Series를 전달하면 benchmark return과 excess return도 계산합니다.

Multifactor 엔진은 현재 날짜 없는 정적 ROE/PBR을 사용하므로 결과의 `research_report`와 `performance`에 `BIASED_RESEARCH_MODE`를 표시합니다. `fundamentals_point_in_time`은 `false`이며, 이 경고가 있는 결과는 point-in-time 펀더멘털을 사용한 검증으로 해석할 수 없습니다.

향후 장기 데이터는 `data/snapshot.py`의 `DataSource`/`DataSnapshot` 인터페이스를 통해 연결할 수 있습니다. snapshot ID, 기준시각, 출처, universe와 metadata provenance를 기록하는 최소 계약만 제공하며 실제 장기·survivorship-free 데이터셋은 포함하지 않습니다.

## 설치 및 개발 환경

Python 3.x가 필요합니다. 현재 지원 버전이 엄밀히 고정되어 있지는 않습니다.

### Python Environment

- 현재 로컬 개발 환경은 Python 3.9.6입니다.
- 다른 Python 3 버전과의 호환성은 아직 체계적으로 검증하지 않았습니다.
- 이는 Python 3.9.6만 지원한다는 의미가 아니며, 지원 버전 범위는 향후 테스트를 통해 확정해야 합니다.
- R3의 `pitindex` 기반 데이터 ingestion은 Python 3.11+ 별도 환경에서 수행하고, 생성된 immutable snapshot만 기본 연구 환경에서 읽습니다. Broker/live-trading runtime을 데이터 수집 환경으로 업그레이드하지 않습니다.

Windows PowerShell 예시:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirments.txt
```

macOS/Linux 예시:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirments.txt
```

현재 의존성 파일 이름은 `requirments.txt`로 잘못 표기되어 있으므로 명령에서도 기존 이름을 사용해야 합니다. 또한 시각화 코드가 사용하는 `matplotlib`이 파일에 누락되어 있습니다. 이 README 작성 작업에서는 의존성 파일을 변경하지 않았습니다.

## 환경변수

repository root에 `.env`를 둘 수 있습니다. 실제 값이나 production credential을 문서·로그·commit에 넣지 마십시오.

```dotenv
CLIENT_ID=your_client_id_here
CLIENT_SECRET=your_client_secret_here
ENABLE_REAL_ORDER=false
```

`.env`, `.env.*`, token 및 account 정보 파일은 `.gitignore` 대상입니다. access token과 계좌번호도 출력하거나 저장소에 저장하지 마십시오.

## Development Workflow

1. 최신 `main`에서 작업을 시작합니다.
2. 작업 목적별 branch를 생성합니다.
3. Codex는 작업 전에 `AGENTS.md`를 확인합니다.
4. 변경은 검증 가능한 작은 단위로 진행합니다.
5. commit 전에 `git diff`와 test 결과를 검토합니다.
6. 하나의 논리적 작업 단위당 하나의 commit을 권장합니다.
7. 중요한 변경은 `main`에서 직접 개발하지 않는 것을 원칙으로 합니다.

## 주요 entry point

모든 현재 entry point는 `if __name__ == "__main__":` guard를 사용하므로 import만으로 OAuth, API 조회, 백테스트, plotting 또는 주문을 실행하지 않습니다.

- `main.py`: 단일 종목의 MA, RSI, volatility breakout, momentum 비교
- `main_rotation.py`: cross-sectional momentum rotation
- `main_multifactor.py`: Multifactor v1
- `main_multifactor_v2.py`: Multifactor v2
- `main_multifactor_v3.py`: Multifactor v3
- `main_multifactor_v4.py`: ATR stop 실험
- `main_multifactor_v4_1.py`: inverse-volatility sizing 실험
- `main_to_real_purchase`: 실제 주문 가능 파일. 명시적인 live 주문 작업 외에는 실행하지 마십시오.

각 main은 현재 실제 Toss API에서 데이터를 요청합니다. 외부 API 사용 승인을 받지 않은 개발·테스트에서는 실행하지 마십시오.

## 안전 경고와 Live Trading Readiness

**현재 시스템은 live trading ready가 아니며 paper trading ready도 아닙니다.**

- live trading은 `ENABLE_REAL_ORDER` 환경변수의 기본값이 `false`인 fail-closed 설정입니다.
- 실제 주문은 live 설정과 실행 시 사용자 확인이 모두 충족되어야 하며, `api/order.py`도 명시적 confirmation이 없으면 주문 POST를 차단합니다.
- paper broker, idempotency, 중복 주문 방지, 잔고 사전 검증, 부분체결, 취소·정정, 재시도, reconciliation이 없습니다.
- 주문 결과와 계좌 응답 전체 출력은 민감정보 노출 위험이 있습니다.
- 시장가 주문의 사전 notional 한도는 아직 구현되지 않았습니다.

사용자가 특정 실주문을 명시적으로 요청하지 않는 한 `buy_stock()`, `sell_stock()`, 주문 endpoint 또는 `main_to_real_purchase`를 실행하지 마십시오.

## Known Issues

- 모든 현재 backtest engine은 종가 signal을 다음 거래일 시가에 체결합니다. Multifactor v4의 ATR stop도 종가에서 stop signal을 확정하고 다음 거래일 시가에 매도합니다.
- commission과 단순 고정 bps slippage는 지원하지만 세금, bid/ask spread의 별도 모델, 환전비용은 아직 없습니다.
- 미국주식 가격과 원화로 표시된 초기 현금 사이에 환율 처리가 없습니다.
- ROE/PBR은 날짜 없는 상수이므로 point-in-time 가용성을 보장하지 않습니다.
- 현재 universe는 사후 선택된 종목일 수 있어 survivorship bias 가능성이 있습니다.
- API 최신 candle 200개만 사용하며 warm-up 후 평가 표본이 약 74~80거래일로 매우 짧습니다.
- benchmark는 호출자가 가격 Series를 제공해야 하며 기본 benchmark dataset은 아직 없습니다.
- 짧은 표본에서 연율화 지표는 통계적으로 의미가 약하며, risk-free rate의 외부 입력은 아직 지원하지 않습니다.
- snapshot/data-source 인터페이스는 있으나 실제 장기 데이터 저장소와 실험 결과 영속화는 아직 없습니다.
- API timeout, retry, exception handling 및 schema validation이 부족합니다.
- 자동화 테스트와 CI가 없습니다.
- `requirments.txt`는 `requirements.txt`의 오타이며 `matplotlib`도 누락되어 있습니다. 이번 작업에서는 변경하지 않았습니다.
- multifactor 버전 파일과 main 파일의 중복이 많습니다.

## 과거 실험 결과에 대한 주의

`ReadMe.txt`에 기록된 수익률, MDD, 승률은 **검증되지 않은 historical experimental result**입니다. 동일 종가 신호·체결에 따른 look-ahead bias, 짧은 표본, 거래비용·slippage·benchmark 부재, 수동 펀더멘털의 기준일 불명확성 때문에 전략 성능의 증거로 간주해서는 안 됩니다.

## Roadmap

### P0 — Safety / Critical Correctness

- live order를 기본 비활성화하고 paper/live 실행 계층 분리
- 모든 executable module에 main guard 적용
- 주문 금액 한도, 중복 방지, 계좌·잔고 검증 및 kill switch 도입
- signal timestamp와 다음 거래 가능 시점의 execution 분리
- USD/KRW 등 통화 및 환율 단위 명시

### P1 — Reliable Backtesting

**Research-ready baseline 완료.** 현재 범위는 institutional-grade historical data platform을 포함하지 않습니다.

- commission/slippage 공통 execution model
- 공통 목표비중 조정과 평균 원가/실현·미실현손익 accounting
- next-open execution과 signal/execution timestamp 분리
- benchmark 입력 및 CAGR, volatility, Sharpe, Sortino, Calmar, turnover
- 정적 ROE/PBR 사용 시 `BIASED_RESEARCH_MODE` 강제 표시
- 장기 데이터 연결을 위한 최소 `DataSource`/`DataSnapshot` 인터페이스

세금·FX·spread 세분화, 실제 point-in-time fundamental, survivorship-free universe와 장기 adjusted dataset은 baseline의 알려진 한계이며 이번 P1 종료 범위에는 포함하지 않습니다.

### R1 — Baseline Strategy / Factor Research

- 공통 데이터 구간과 benchmark를 먼저 고정하고 baseline 전략 선정
- factor 가설, 계산 시점, 기대 방향과 평가 기준을 사전 정의
- in-sample 성과 최대화 대신 out-of-sample/walk-forward 비교
- turnover와 거래비용 적용 전후 성과를 함께 평가
- parameter sensitivity와 factor 간 상관·중복 노출 점검

### P2 — Research Infrastructure

- 중복 버전을 하나의 engine + config 구조로 통합
- data, signal, selection, allocation, execution, metrics 분리
- 실험 parameter·data version·결과 metadata 저장
- unit/integration test와 CI 구축
- out-of-sample, walk-forward 및 parameter sensitivity 분석

### P3 — Paper/Live Trading Infrastructure

- paper broker adapter와 broker interface
- 주문 상태 머신 및 부분체결·취소·정정 처리
- 내부 원장과 broker 계좌 reconciliation
- scheduler, 휴장일, retry/backoff, rate limiting
- structured logging, monitoring, alert 및 장애 복구

### P4 — Advanced Quant / ML

- market regime과 동적 factor weighting
- transaction-cost-aware portfolio optimization
- purged/embargoed time-series validation
- factor/sector exposure 및 risk budgeting
- 충분한 데이터 확보 후 ML 예측, uncertainty 및 model drift 관리

P4는 P0~P2의 데이터·회계·검증 기반이 갖춰진 뒤 진행해야 합니다.
