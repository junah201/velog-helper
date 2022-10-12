function createElement(tag, attrs) {
	const keys = Object.keys(attrs || {});
	const el = document.createElement(tag);
	for (let i = 0; i < keys.length; ++i) {
		el.setAttribute(keys[i], attrs[[keys[i]]]);
	}
	return el;
}

function createNoticeItems() {
	const noticeItemsDiv = createElement("div", { class: "notice-item-div" });
	chrome.runtime.sendMessage(
		{
			message: "get_new_post",
		},
		(response) => {
			response.data.forEach(function (item, index, array) {
				console.log(item);
				const itemDiv = createElement("div", { class: "notice-item" });
				const itemBlogImg = createElement("div", {
					style: `background-image: url(${item.user_img})`,
					class: "notice-blog-img",
				});
				const itemTitle = createElement("a", {
					href: `https://velog.io/@${item.user}/${item.link}`,
				});
				itemTitle.innerHTML = item.title;
				const itemDate = createElement("div", { class: "notice-date" });
				itemDate.innerHTML = item.created_at.substring(5, 10);
				itemDiv.append(itemBlogImg, itemTitle, itemDate);
				noticeItemsDiv.append(itemDiv);
			});
		}
	);
	return noticeItemsDiv;
}

function createBlogItems() {
	const blogItemsDiv = createElement("div", { class: "blog-item-div" });
	chrome.runtime.sendMessage(
		{
			message: "get_blogs",
		},
		(response) => {
			console.log(response);
			console.log(response.blogs);
			response.blogs.forEach(function (item, index, array) {
				const blogItemDiv = createElement("div", { class: "blog-item" });
				const blogImg = createElement("img", {
					class: "blog-img",
					src: item.profile_img,
				});
				const blogName = createElement("a", {
					class: "blog-name",
					href: `https://velog.io/@${item.id}`,
					target: "_blank",
				});
				const blogRemoveButton = createElement("button", {
					class: "blog-remove-button",
					value: item.id,
				});
				blogName.innerHTML = item.id;
				blogItemDiv.append(blogImg, blogName, blogRemoveButton);
				blogItemsDiv.append(blogItemDiv);

				blogRemoveButton.addEventListener("click", (e) => {
					chrome.runtime.sendMessage(
						{
							message: "delete_bookmark",
							payload: e.target.value,
						},
						(response) => {
							if (response.message === "success") {
								console.log("success delete bookmark");
								e.path[1].classList.add("undisplay");
							}
						}
					);
				});
			});
		}
	);
	return blogItemsDiv;
}

function createSettings() {
	const SettingsDiv = createElement("div", { class: "setting-div" });
	SettingsDiv.innerHTML = "아직 준비중이에요...";
	return SettingsDiv;
}
