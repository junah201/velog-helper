const Constants = {
	BACKEND_URL: "https://velog-helper.herokuapp.com",
};

function registUser() {
	chrome.storage.local.get(["user_id", "user_email"], (data) => {
		fetch(`${Constants.BACKEND_URL}/user`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				id: data.user_id,
				email: data.user_email,
			}),
		}).then((response) => console.log(response));
	});
}

chrome.runtime.onInstalled.addListener(() => {
	chrome.identity.getProfileUserInfo(function (userInfo) {
		// 로그인 되어 있지 않은 유저일 경우 -> 타임스템프와 IP를 임시 아이디로 지정
		// TODO : 임시 아이디를 만드는 과정에서 해쉬 등 암호화 과정이 필요함
		if (userInfo.email === "") {
			fetch("https://api.ipify.org?format=json", {
				method: "GET",
				headers: {
					"Content-Type": "application/json",
				},
			})
				.then((response) => {
					return response.json();
				})
				.then((data) => {
					chrome.storage.local.set({
						user_id: "" + new Date().getTime() + data.ip,
						user_email: userInfo.email,
					});
				})
				.then(registUser);
		}
		// 로그인 되어 있는 유저 일 경우 -> 크롬 아이디 이용
		else {
			chrome.storage.local
				.set({
					user_id: userInfo.id,
					user_email: userInfo.email,
				})
				.then(registUser);
		}
	});
});

async function onUpdated(tabId) {
	const tab = await chrome.tabs.get(tabId);
	if (tab.status == "complete" && /^http/.test(tab.url)) {
		chrome.scripting
			.insertCSS({
				target: { tabId: tab.id },
				files: ["./src/notice.css"],
			})
			.then(() => {
				chrome.scripting
					.executeScript({
						target: { tabId: tab.id },
						files: ["./src/util.js", "./src/notice.js"],
					})
					.then(() => {
						console.log("SUCCES add notice button");
					});
			})
			.catch((err) => console.log(err));
	}
	// 개인 블로그 메인 페이지 혹은 포스트 페이지라면?
	if (
		tab.status == "complete" &&
		/^http/.test(tab.url) &&
		tab.url != "https://velog.io/" &&
		tab.url[17] === "@"
		/*
    tab.url.split("/").slice(-1) != "" &&
    tab.url.split("/").length === 4
    */
	) {
		chrome.scripting
			.insertCSS({
				target: { tabId: tab.id },
				files: ["./src/bookmark.css"],
			})
			.then(() => {
				chrome.scripting
					.executeScript({
						target: { tabId: tab.id },
						files: ["./src/util.js", "./src/bookmark.js"],
					})
					.then(() => {});
			})
			.catch((err) => console.log(err));
	}
}

chrome.tabs.onUpdated.addListener(async (tabID, changeInfo, tab) => {
	await onUpdated(tabID);
});

chrome.tabs.onReplaced.addListener(async (addedTabId, removedTabId) => {
	await onUpdated(addedTabId);
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
	if (request.message === "add_bookmark") {
		chrome.storage.local.get(["user_id", "user_email"], (data) => {
			fetch(
				`${Constants.BACKEND_URL}/${data.user_id}/blog?blog_id=${request.payload}`,
				{
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
				}
			)
				.then((response) => {
					return response.json();
				})
				.then((data) => {
					sendResponse({ message: "success" });
					return;
				});
		});
		return true;
	} else if (request.message === "delete_bookmark") {
		chrome.storage.local.get(["user_id", "user_email"], (data) => {
			fetch(
				`${Constants.BACKEND_URL}/${data.user_id}/blog?blog_id=${request.payload}`,
				{
					method: "DELETE",
					headers: {
						"Content-Type": "application/json",
					},
				}
			)
				.then((response) => {
					return response.json();
				})
				.then((data) => {
					sendResponse({ message: "success" });
					return;
				});
		});
		return true;
	} else if (request.message === "get_new_post") {
		chrome.storage.local.get(["user_id", "user_email"], (data) => {
			fetch(`${Constants.BACKEND_URL}/${data.user_id}/archive`, {
				method: "GET",
				headers: {
					"Content-Type": "application/json",
				},
			})
				.then((response) => {
					console.log(response);
					return response.json();
				})
				.then((data) => {
					console.log(data);
					sendResponse({ message: "success", data: data });
					return;
				});
		});
		return true;
	} else if (request.message === "is_bookmarked") {
		chrome.storage.local.get(["user_id", "user_email"], (data) => {
			fetch(
				`${Constants.BACKEND_URL}/${data.user_id}/is_bookmarked?blog_id=${request.payload}`,
				{
					method: "GET",
					headers: {
						"Content-Type": "application/json",
					},
				}
			)
				.then((response) => {
					return response.json();
				})
				.then((data) => {
					sendResponse({
						message: "success",
						is_bookmarked: data.is_bookmarked,
					});
					return;
				});
		});
		return true;
	} else if (request.message === "get_blogs") {
		chrome.storage.local.get(["user_id"], (data) => {
			fetch(`${Constants.BACKEND_URL}/${data.user_id}/blogs`, {
				method: "GET",
				headers: {
					"Content-Type": "application/json",
				},
			})
				.then((response) => {
					console.log(response);
					return response.json();
				})
				.then((data) => {
					console.log(data);
					sendResponse({
						message: "success",
						blogs: data.blogs,
					});
					return;
				});
		});
		return true;
	}
});

// TODO : 나중에 고민...
/*
} else if (request.message === "update_new_post") {
    chrome.storage.local.get(["user_id", "user_email"], (data) => {
      fetch(`${Constants.BACKEND_URL}/update_new_post?user_id=${data.user_id}`, {
        method: "GET",
      })
        .then((response) => {
          return response.json();
        })
        .then((data) => {
          sendResponse({ message: "success" });
          return;
        });
    });
    return true;
    */
