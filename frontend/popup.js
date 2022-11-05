const Constants = {
	BACKEND_URL: "https://velog-helper.herokuapp.com",
};

const blogItmes = createBlogItems();
const noticeItems = createNoticeItems();

document.querySelector("main").append(blogItmes);
document.querySelector("main").append(noticeItems);

const blogButton = document.getElementById("blog-button");
const noticeButton = document.getElementById("notice-button");
const settingButton = document.getElementById("setting-button");

const undisplayDivs = () => {
	const divs = document.querySelectorAll("main > div");
	for (div of divs) {
		div.classList.remove("display");
	}
};

blogButton.addEventListener("click", () => {
	undisplayDivs();
	document.querySelector(".blog-item-div").classList.add("display");
});
noticeButton.addEventListener("click", () => {
	undisplayDivs();
	document.querySelector(".notice-item-div").classList.add("display");
});
settingButton.addEventListener("click", () => {
	undisplayDivs();
	document.querySelector(".setting-div").classList.add("display");
});

document
	.getElementById("setting-email-button")
	.addEventListener("click", () => {
		const email = document.getElementById("setting-email-input");
		if (email.validationMessage) {
			alert(email.validationMessage);
			return;
		}
		chrome.runtime.sendMessage(
			{
				message: "veloghelper-change_email",
				payload: email.value,
			},
			(response) => {
				alert(
					`이메일이 수정 완료되었습니다.\n이제 ${email.value}로 새 글 알림이 수신됩니다.`
				);
			}
		);
	});
