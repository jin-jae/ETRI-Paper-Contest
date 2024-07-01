# (TODO: 논문 제목 추후 추가)


## 제3회 ETRI 휴먼이해 인공지능 논문경진대회

### ❓ 대회 소개
- 기간: 2024.04 ~ 2024.06
- 주제: 라이프로그 데이터를 이용한 수면, 감정, 스트레스 인식 및 추론

### 🧑🏻‍💻 팀원 소개
| ![jin-jae](https://avatars.githubusercontent.com/u/97018331) | ![maj34](https://avatars.githubusercontent.com/u/75362328) | ![Chokeunhee](https://avatars.githubusercontent.com/u/43236895) | ![eunjeechoi](https://avatars.githubusercontent.com/u/97671436) |
| :---: | :---: | :---: | :---: |
| 김진재 | 마민정 | 조근희 | 최은지 |
| [Github](https://github.com/jin-jae) | [Github](https://github.com/maj34) | [Github](https://github.com/Chokeunhee) | [Github](https://github.com/eunjeechoi) |
| [E-mail](mailto:jinjae.dev@gmail.com) | [E-mail](mailto:minjeong_ma@korea.ac.kr) | [E-mail] | [E-mail](mailto:eun09ji@korea.ac.kr) |


## 데이터 및 코드 설명

### 💽 활용 데이터
- Train: [ETRI_Lifelog_Dataset_2020](https://nanum.etri.re.kr/share/schung/ETRILifelogDataset2020?lang=En_us)
- Validation / Test: [비공개 데이터셋]

### 💻 구동 환경
(TODO: 실험 환경과 동일한 Dockerfile을 추가하였습니다.)
|  | Environment |
| :---: | :---: |
| OS | ubuntu18.04 |
| Python | 3.8.19 |

requirements는 다음과 같이 설치할 수 있습니다:
`pip install -r src/mvts_transformer/failsafe_requirements.txt`
`pip install scikit_learn`

### 📖 실행 방법

#### 파일 구조
전처리 실행 전 파일 구조는 다음과 같이 세팅해야 합니다.  
`tree -hl -L 4`
```
[ 160]  .
├── [1.3K]  README.md
└── [  31]  data_raw
    ├── [9.5K]  README_2020.txt
    ├── [5.6G]  user01-06.7z
    ├── [5.9G]  user07-10.7z
    ├── [3.5G]  user11-12.7z
    ├── [5.1G]  user21-25.7z
    ├── [5.1G]  user26-30.7z
    ├── [1.1K]  user_info_2020.csv
    ├── [ 73K]  user_sleep_2020.csv
    ├── [ 89K]  user_survey_2020.csv
    └── [7.0G]  휴먼이해2024.zip
    ...
```
`README_2020.txt`, `user*.7z`, `user_*_2020.csv` 파일은 활용 데이터 중 Train을 통해, \
`휴먼이해2024.zip` 파일은 Validation / Test를 통해 구할 수 있습니다.

#### 모델 실행 방법
모델은 다음 두 가지를 활용하여 예측하였습니다.
- mvts_transformer : `./src/mvts_transformer/mvts_transformer_final.ipynb`
- Multi Output Classifier : `./src/multi_output_classifier.ipynb`

위 두 `ipynb` 파일을 각각 실행한 이후, `./src/make_final.py`를 이용하여 두 실행 결과를 합하면 됩니다.
