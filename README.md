<p align="center">
  <img src="./frontend/icons/icon128.png" width=100/>
</p>
<p align="center">
  Velog Helper
  <br/>  
  Velog을 확장된 기능과 함께 사용해보세요.
</p>

# 기능

### Velog Helper는 다음과 같은 기능을 지원합니다.

- 블로그 북마크
- 블로그 새 글 알림

### Velog Helper는 다음과 같은 기능을 지원할 예정입니다.

- 새 글 에디터에서 더 많은 단축키 지원
  (예 : art + ↑ 줄 이동)

# 설치 방법

1. 크롬확장프로그램 스토어에서 `Velog Helper`를 검색하거나 [링크](https://chrome.google.com/webstore/detail/velog-helper/limdbpmjjehbmlnmkmaadbkklkmohbag?hl=ko)를 통해서 접속해주세요.
2. `크롬에 추가` 버튼을 통해서 다운로드 해주세요.
3. 이후 Velog 메인화면에 들어가면 종 모양의 알림버튼이 생깁니다.
![](https://velog.velcdn.com/images/junah201/post/15ccd218-ed72-4fc2-ba0f-a2288d8954c6/image.png)
4. 이 버튼을 누르면 아직 아무런 글이 표시되지 않을텐데, 아무 블로그 메인화면에 들어가서 별표시의 북마크 버튼을 눌러주세요

![](https://velog.velcdn.com/images/junah201/post/fa1e8332-4cea-4bc5-b833-e88ad811f48b/image.png)

만약 해당 블로그가 이미 Velog Helper에 등록되어 있다면 바로 새 글 알림 목록에 뜨지만, 등록되어 있지 않다면 15분 이내로 목록에 자동으로 추가됩니다.
5. 만약 크롬이 구글 로그인이 되어 있다면 자동으로 해당 이메일을 가져와서 알림을 전송하지만, 로그인이 안되어있거나 웨일 등의 다른 브라우저를 사용중이면 오른쪽 위 팝업에서 이메일을 등록해주세요.

![](https://velog.velcdn.com/images/junah201/post/27bf42aa-4629-4eeb-9599-be5aede95dd8/image.png)

# 실행 방법

PR을 위한 백엔드 실행 방법
```
pip install -r requirements.txt
cd .\backend\
uvicorn app.main:app --reload
```

PR을 위한 프론트엔드 실행 방법
```
크롬확장프로그램 개발자 모드를 킨다.
`압축 해제된 확장프로그램을 로드합니다.`에서 velog-helper/frontend 폴더를 선택한다.
```

# 관련 문서

- [개인정보처리방침](https://junah.notion.site/e297108af58744809dd6b9f1db49efe0)

# 후원

개발자는 언제나 가난합니다... 서버 유지비...

<a href="https://toss.me/junah">
  <img src="https://static.toss.im/tds/favicon/favicon.ico" width=50/>
</a>
<a href="https://qr.kakaopay.com/FLnSPzJZZ">
  <img src="https://t1.daumcdn.net/kakaopay/icons/favicon.ico" width=50/>
</a>

| 날짜       | 성함   | 금액     | 메시지 | 수단   | 깃허브 |
|------------|--------|----------|--------|--------|--------| 
| 2022.11.24 | 박수혁 | 10,000원 | 박수혁 | 카카오 | |
| 2022.11.24 | 윤혜원 | 10,000원 | 윤혜원 | 카카오 | |
| 2022.11.25 | 위준우 | 10,000원 | 위준우 | 카카오 | [@wijoonwu](https://github.com/wijoonwu) |

# 기타 문의

Email : junah.dev@gmail.com

Discord : Junah#6689
