#  PyComix 🐍📚

**PyComix**는 파이썬으로 만든 간단하고 강력한 만화 뷰어 애플리케이션입니다. 좋아하는 만화를 쉽고 편리하게 즐겨보세요.

![PyComix-screenshot](https://via.placeholder.com/700x400.png?text=PyComix+App+Screenshot)
*(이곳에 실제 앱 스크린샷을 추가하세요)*

## ✨ 주요 기능

* **다양한 포맷 지원**: `.cbz`, `.cbr`, `.zip`, `.rar` 등 주요 만화 파일 형식을 지원합니다.
* **직관적인 UI**: 사용하기 쉬운 인터페이스로 누구나 편리하게 만화를 볼 수 있습니다.
* **페이지 넘김**: 키보드 단축키와 마우스 클릭으로 부드럽게 페이지를 넘길 수 있습니다.
* **라이브러리 관리**: 가지고 있는 만화 파일을 라이브러리에 추가하고 관리할 수 있습니다. (구현 예정)
* **크로스 플랫폼**: 윈도우, macOS, 리눅스에서 모두 사용 가능합니다.

## 🚀 설치 및 실행 방법

이 프로젝트를 로컬 컴퓨터에서 실행하려면 다음 단계를 따르세요.

**1. 저장소 복제(Clone)**

```bash
git clone [https://github.com/your-username/PyComix.git](https://github.com/your-username/PyComix.git)
cd PyComix
```

**2. 가상 환경 생성 및 활성화**

```bash
# Python 가상 환경 생성
python -m venv venv

# 윈도우
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. 의존성 패키지 설치**

프로젝트에 필요한 라이브러리를 설치합니다.

```bash
pip install -r requirements.txt
```
*(실제 사용한 라이브러리를 `requirements.txt` 파일에 꼭 명시해주세요.)*

**4. 애플리케이션 실행**

```bash
python main.py
```

## 🛠️ 기술 스택

* **언어**: Python 3
* **GUI 프레임워크**: PyQt6 (또는 PySide6)
* **이미지 처리**: Pillow
* **패키징**: PyInstaller

## 📦 배포 (Packaging)

**PyInstaller**를 사용하여 독립적인 실행 파일(`.exe`, `.app`)을 만들 수 있습니다.

```bash
# --onefile: 하나의 실행 파일로 생성
# --windowed: 실행 시 콘솔 창 숨기기
pyinstaller --onefile --windowed main.py --name PyComix
```

## 🤝 기여하기 (Contributing)

이 프로젝트에 기여하고 싶으신가요? 언제나 환영입니다!

1.  이 저장소를 Fork 하세요.
2.  새로운 기능 브랜치를 만드세요 (`git checkout -b feature/AmazingFeature`).
3.  변경 사항을 커밋하세요 (`git commit -m 'Add some AmazingFeature'`).
4.  브랜치에 Push 하세요 (`git push origin feature/AmazingFeature`).
5.  Pull Request를 열어주세요.

## 📄 라이선스

이 프로젝트는 **MIT 라이선스**를 따릅니다. 자세한 내용은 `LICENSE` 파일을 참고하세요.

---
*Made with ❤️ by [Sungkuk Park](https://github.com/sungkukpark)*