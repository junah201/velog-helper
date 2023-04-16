function createBookmarkButton() {
	const bookmarkButton = createElement("button", { class: "bookmark-button" });
	bookmarkButton.innerHTML =
		'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M12 .587l3.668 7.568 8.332 1.151-6.064 5.828 1.48 8.279-7.416-3.967-7.417 3.967 1.481-8.279-6.064-5.828 8.332-1.151z"/></svg>';

	bookmarkButton.addEventListener("click", () => {
		if (bookmarkButton.classList.contains("yellow-bookmark-button")) {
			bookmarkButton.classList.remove("yellow-bookmark-button");
			browser.runtime.sendMessage({
				message: "delete_bookmark",
				payload: window.location.pathname.split("/")[1].substring(1),
			});
		} else {
			bookmarkButton.classList.add("yellow-bookmark-button");
			browser.runtime.sendMessage({
				message: "add_bookmark",
				payload: window.location.pathname.split("/")[1].substring(1),
			});
		}
	});

	browser.runtime.sendMessage(
		{
			message: "is_bookmarked",
			payload: window.location.pathname.split("/")[1].substring(1),
		},
		(response) => {
			if (response.is_bookmarked) {
				bookmarkButton.classList.add("yellow-bookmark-button");
			} else {
				bookmarkButton.classList.remove("yellow-bookmark-button");
			}
		}
	);

	return bookmarkButton;
}

if (document.querySelector(".bookmark-button") == null) {
	var blogProfile = document.querySelector("div > div.name");
	if (!!blogProfile) {
		var bookmarkButton = createBookmarkButton();
		blogProfile.append(bookmarkButton);
		console.log("SUCCES add bookmark button in blog profile");
	}

	var username = document.querySelector("div.information > span.username");
	if (username != null && username != undefined) {
		var bookmarkButton = createBookmarkButton();
		username.after(bookmarkButton);
		console.log("SUCCES add bookmark button in top of post");
	}

	var followerIndicatorContainer = document.querySelector(".description");
	var originalFollowerIndicator = document.querySelector(".follower-indicator");
	if (!!followerIndicatorContainer && !originalFollowerIndicator) {
		followerIndicatorContainer.append(createElement("br", {}));
		browser.runtime.sendMessage(
			{
				message: "veloghelper-get_followers",
				payload: window.location.pathname.split("/")[1].substring(1),
			},
			(response) => {
				if (response?.followers == "Blog not found") return;
				var followerIndicator = createElement("smail", {
					class: "follower-indicator",
				});
				followerIndicator.innerHTML = `팔로워 ${response?.followers || 0}명`;
				// 중복 추가 방지
				if (!document.querySelector(".follower-indicator")) {
					followerIndicatorContainer.append(followerIndicator);
					console.log("SUCCES add follower indicator");
				}
			}
		);
	}
}
