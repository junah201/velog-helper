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

const introDiv = document.querySelector(".intro-div");
const blogDiv = document.querySelector(".blog-item-div");
const noticeDiv = document.querySelector(".notice-item-div");
const settingDiv = document.querySelector(".setting-div");

const undisplayDivs = () => {
	introDiv.classList.remove("display");
	blogDiv.classList.remove("display");
	noticeDiv.classList.remove("display");
	settingDiv.classList.remove("display");
};

blogButton.addEventListener("click", () => {
	undisplayDivs();
	blogDiv.classList.add("display");
});
noticeButton.addEventListener("click", () => {
	undisplayDivs();
	noticeDiv.classList.add("display");
});
settingButton.addEventListener("click", () => {
	undisplayDivs();
	settingDiv.classList.add("display");

	chrome.runtime
		.sendMessage({
			message: "veloghelper-get_email",
		})
		.then((data) => {
			document.querySelector("#current-email-span").textContent = data.email;
		});
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
				document.querySelector("#current-email-span").textContent = email.value;
			}
		);
	});
