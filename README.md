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

# 설치 방법

## 등록 이전 (2022.08.14 ~ )

크롬 확장프로그램 스토어에 등록 중입니다. 등록 전까지는 임시로 직접 설치해서 사용해주세요. (2022.08.14 기준 검토 중)

가장 최신 릴리스를 설치해주세요. [V0.1.0](https://github.com/junah201/velog-helper/releases/tag/v0.1.0)
설치 후 압축을 풀어주세요. (반디집 이용 권장)

`chrome://extensions/`에 접속합니다.

![image](https://user-images.githubusercontent.com/75025529/184528353-e96b6704-11d3-4050-9291-5c6ee950692e.png)

오른쪽 위에 `개발자 모드`를 활성화 해주세요.

![image](https://user-images.githubusercontent.com/75025529/184528407-f859f358-0319-4f83-962b-f79db052f2ca.png)

왼쪽 위에 `압축해제된 확장 프로그램을 로드합니다.`를 선택해주세요.
이후 압축 해제한 폴더를 선택해주세요.

![image](https://user-images.githubusercontent.com/75025529/184528604-ca6b3bc1-f5c4-48c6-a72e-ea9c88ee0f97.png)

이후 로딩 된 Velog Helper 를 이용해주세요.

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
