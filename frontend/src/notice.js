function add_notice_button(div) {
	var noticeButton = createElement("button", {
		class: "notice-button sc-dlVxhl bluJY",
	});
	noticeButton.innerHTML =
		'<svg class = "GHcMM" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M15.137 3.945c-.644-.374-1.042-1.07-1.041-1.82v-.003c.001-1.172-.938-2.122-2.096-2.122s-2.097.95-2.097 2.122v.003c.001.751-.396 1.446-1.041 1.82-4.667 2.712-1.985 11.715-6.862 13.306v1.749h20v-1.749c-4.877-1.591-2.195-10.594-6.863-13.306zm-3.137-2.945c.552 0 1 .449 1 1 0 .552-.448 1-1 1s-1-.448-1-1c0-.551.448-1 1-1zm3 20c0 1.598-1.392 3-2.971 3s-3.029-1.402-3.029-3h6z"/></svg>';

	div.prepend(noticeButton);

	var noticeDiv = createElement("div", {
		class: "notice-container undisplay",
	});
	noticeMenuDiv = createElement("div", { class: "notice-menu-div" });
	noticeMenuTitle = createElement("div", {});
	noticeMenuTitle.innerHTML = "새로운 글 목록";

	noticeMenuDiv.append(noticeMenuTitle);

	noticeDiv.append(noticeMenuDiv, createNoticeItems());

	div.append(noticeDiv);

	noticeButton.addEventListener("click", () => {
		if (noticeDiv.classList.contains("undisplay")) {
			noticeDiv.classList.remove("undisplay");
		} else {
			noticeDiv.classList.add("undisplay");
		}
	});
}

if (document.querySelector(".notice-button") == null) {
	const divs = document.querySelectorAll(".sc-llYSUQ.bqeVpK");
	divs.forEach(function (div) {
		add_notice_button(div);
	});
}
