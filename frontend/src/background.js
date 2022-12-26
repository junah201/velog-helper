const Constants = {
	BACKEND_URL: "https://velog-helper.herokuapp.com",
	// BACKEND_URL: "http://localhost:8000"
};

globalThis.browser = (function () {
	return (
		globalThis.msBrowser ||
		globalThis.browser ||
		globalThis.chrome ||
		globalThis.whale
	);
})();

function registUser() {
	browser.storage.local.get(["user_id", "user_email"], (data) => {
		fetch(`${Constants.BACKEND_URL}/user`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				id: data.user_id,
				email: data.user_email,
			}),
		});
	});
}

browser.runtime.onInstalled.addListener(() => {
	// whale 브라우저에서는 identity api 지원 중단으로 인해 예외처리 필요
	if (!globalThis.whale) {
		browser.identity.getProfileUserInfo(function (userInfo) {
			// TODO : 임시 아이디를 만드는 과정에서 해쉬 등 암호화 과정이 필요함
			// 로그인 되어 있지 않은 유저일 경우 -> 타임스템프와 IP를 임시 아이디로 지정
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
						browser.storage.local.set({
							user_id: "" + new Date().getTime() + data.ip,
							user_email: userInfo.email,
						});
					})
					.then(registUser);
			}
			// 로그인 되어 있는 유저 일 경우 -> 크롬 아이디 이용
			else {
				browser.storage.local
					.set({
						user_id: userInfo.id,
						user_email: userInfo.email,
					})
					.then(registUser);
			}
		});
	} else {
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
				browser.storage.local.set({
					user_id: "" + new Date().getTime() + data.ip,
					user_email: "",
				});
			})
			.then(registUser);
	}

	// 사용 설명서 페이지를 새 탭으로 열기
	browser.tabs.create({
		url: `${Constants.BACKEND_URL}/guide`,
	});
});

async function onUpdated(tabId) {
	const tab = await browser.tabs.get(tabId);
	if (tab.status == "complete" && /^http/.test(tab.url)) {
		browser.scripting
			.insertCSS({
				target: { tabId: tab.id },
				files: ["./src/notice.css"],
			})
			.then(() => {
				browser.scripting.executeScript({
					target: { tabId: tab.id },
					files: ["./src/util.js", "./src/notice.js"],
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
		browser.scripting
			.insertCSS({
				target: { tabId: tab.id },
				files: ["./src/bookmark.css"],
			})
			.then(() => {
				browser.scripting
					.executeScript({
						target: { tabId: tab.id },
						files: ["./src/util.js", "./src/bookmark.js"],
					})
					.then(() => {});
			})
			.catch((err) => console.log(err));
	}
}

browser.tabs.onUpdated.addListener(async (tabID, changeInfo, tab) => {
	await onUpdated(tabID);
});

browser.tabs.onReplaced.addListener(async (addedTabId, removedTabId) => {
	await onUpdated(addedTabId);
});

browser.runtime.onMessage.addListener((request, sender, sendResponse) => {
	if (request.message === "add_bookmark") {
		browser.storage.local.get(["user_id", "user_email"], (data) => {
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
		browser.storage.local.get(["user_id", "user_email"], (data) => {
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
		browser.storage.local.get(["user_id", "user_email"], (data) => {
			fetch(`${Constants.BACKEND_URL}/${data.user_id}/archive`, {
				method: "GET",
				headers: {
					"Content-Type": "application/json",
				},
			})
				.then((response) => {
					return response.json();
				})
				.then((data) => {
					sendResponse({ message: "success", data: data });
					return;
				});
		});
		return true;
	} else if (request.message === "is_bookmarked") {
		browser.storage.local.get(["user_id", "user_email"], (data) => {
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
		browser.storage.local.get(["user_id"], (data) => {
			fetch(`${Constants.BACKEND_URL}/${data.user_id}/blogs`, {
				method: "GET",
				headers: {
					"Content-Type": "application/json",
				},
			})
				.then((response) => {
					return response.json();
				})
				.then((data) => {
					sendResponse({
						message: "success",
						blogs: data.blogs,
					});
					return;
				});
		});
		return true;
	} else if (request.message === "veloghelper-change_email") {
		browser.storage.local.get(["user_id"], (data) => {
			fetch(
				`${Constants.BACKEND_URL}/${data.user_id}/email?email=${request.payload}`,
				{
					method: "Post",
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
					});
					return;
				});
		});
		return true;
	} else if (request.message === "veloghelper-get_email") {
		/**
		 * Backend에서 email을 가져오는 코드
		 * @author myoun
		 */

		browser.storage.local.get(["user_id"], (data) => {
			fetch(`${Constants.BACKEND_URL}/user?user_id=${data.user_id}`, {
				method: "GET",
				headers: {
					"Content-Type": "application/json",
				},
			})
				.then((response) => {
					return response.json();
				})
				.then((data) => {
					sendResponse({
						message: "success",
						email: data.email,
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
    browser.storage.local.get(["user_id", "user_email"], (data) => {
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
