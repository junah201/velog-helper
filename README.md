<p align="center">
  <img src="./frontend/icons/icon128.png" width=100/>
</p>
<br/>
<p align="center">
  Velog Helper
  <br/>  
  Velog을 확장된 기능과 함께 사용해보세요.
</p>

# 기능

## Velog Helper는 다음과 같은 기능을 지원합니다.

- 블로그 북마크
- 블로그 새 글 알림

## Velog Helper는 다음과 같은 기능을 지원할 예정입니다.

- 새 글 에디터에서 더 많은 단축키 지원
  (예 : art + ↑ 줄 이동)

# 설치 방벙
- 일반적인 방법
1. [Velog Helper](https://chrome.google.com/webstore/detail/velog-helper/limdbpmjjehbmlnmkmaadbkklkmohbag?hl=ko)에 들어간다.
2. 설치한다.

- 대안책
1. [크롬 확장 프로그램 스토어](https://chrome.google.com/webstore/category/extensions?hl=ko)에 접속한다.
2. `Velog Helper`를 검색한다.
3. Velog Helper를 설치한다.

# 개발 예정 (TO DO)

## Velog Helper 탭

![](https://velog.velcdn.com/images/junah201/post/0f57a773-eef2-4420-bcab-7744fd7befc0/image.png)

크롬 확장에서 Velog Helper를 클릭시 나오는 창에 아직은 아무 것도 없지만 북마크된 블로그 목록을 볼 수 있고, 관리할 수 있는 추가 탭을 제작할 예정입니다.

## 확장 프로그램 설치 시 튜토리얼 탭

크롬 확장 프로그램이 설치되었을 때 사용법을 안내하는 튜토리얼 탭의 필요성을 느껴 제작할 예정입니다.

# 버그

Velog Helper는 아직 버그가 많아요 ㅠㅠ 이슈 및 PR은 항상 환영합니다.

## 북마크 버튼 반복클릭 시 버그

북마크 버튼을 광클하면 노란색으로 북마크가 되어 있다고 나오는데 실제로는 북마크가 안되어 있습니다. 백엔드 서버와의 지연 문제로 예상됩니다.
새로고침 할 경우 다시 로딩해서 불러오기 때문에 해결됩니다.

## 모바일 레이아웃

모바일에서 레이아웃이 정상적으로 보이지 않는 문제가 존재합니다.

![image](https://velog.velcdn.com/images/junah201/post/c66c69dd-7422-492f-82a7-ae797f59f836/image.png)
