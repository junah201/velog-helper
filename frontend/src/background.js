const Constants = {
	BACKEND_URL:
		"https://3t4g2w8kcf.execute-api.ap-northeast-2.amazonaws.com/prod",
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
				user_id: data.user_id,
				email: data.user_email,
			}),
		});
	});
}

browser.runtime.onInstalled.addListener((details) => {
	// 초기 설치 시에만 실행
	if (details.reason !== "install") {
		return;
	}
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
				files: ["./src/notice.css", "./src/scroll.css"],
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
	) {
		browser.scripting
			.insertCSS({
				target: { tabId: tab.id },
				files: ["./src/bookmark.css"],
			})
			.then(() => {
				browser.scripting.executeScript({
					target: { tabId: tab.id },
					files: ["./src/util.js", "./src/bookmark.js"],
				});
			})
			.catch((err) => console.log(err));
	}
}

browser.tabs.onUpdated.addListener(async (tabID, changeInfo, tab) => {
	console.log("onUpdated");
	await onUpdated(tabID);
});

browser.tabs.onReplaced.addListener(async (addedTabId, removedTabId) => {
	console.log("onReplaced");
	await onUpdated(addedTabId);
});

browser.runtime.onMessage.addListener((request, sender, sendResponse) => {
	if (request.message === "add_bookmark") {
		browser.storage.local.get(["user_id", "user_email"], (data) => {
			fetch(
				`${Constants.BACKEND_URL}/user/${data.user_id}/blog/${request.payload}`,
				{
					method: "POST",
					headers: {
						"Content-Type": "application/json",
						Accept: "application/json",
					},
				}
			)
				.then((response) => {
					if (response.status === 204) {
						sendResponse({ message: "success" });
						return;
					}
				})
				.catch((err) => {
					console.log(err);
				});
		});
	} else if (request.message === "delete_bookmark") {
		browser.storage.local.get(["user_id", "user_email"], (data) => {
			fetch(
				`${Constants.BACKEND_URL}/user/${data.user_id}/blog/${request.payload}`,
				{
					method: "DELETE",
					headers: {
						"Content-Type": "application/json",
						Accept: "application/json",
					},
				}
			)
				.then((response) => {
					if (response.status === 204) {
						sendResponse({ message: "success" });
						return;
					}
				})
				.catch((err) => {
					console.log(err);
				});
		});
	} else if (request.message === "get_new_post") {
		browser.storage.local.get(["user_id", "user_email"], (data) => {
			fetch(
				`${Constants.BACKEND_URL}/user/${data.user_id}/posts?skip=0&limit=15`,
				{
					method: "GET",
					headers: {
						"Content-Type": "application/json",
						Accept: "application/json",
					},
				}
			)
				.then((response) => {
					return response.json();
				})
				.then((data) => {
					sendResponse({ message: "success", data: data });
					return;
				})
				.catch((err) => {
					console.log(err);
				});
		});
	} else if (request.message === "is_bookmarked") {
		browser.storage.local.get(["user_id", "user_email"], (data) => {
			fetch(
				`${Constants.BACKEND_URL}/user/${data.user_id}/blog/${request.payload}`,
				{
					method: "GET",
					headers: {
						"Content-Type": "application/json",
						Accept: "application/json",
					},
				}
			)
				.then((response) => {
					if (response.status === 200) {
						sendResponse({
							message: "success",
							is_bookmarked: true,
						});
						return;
					}
					sendResponse({
						message: "success",
						is_bookmarked: false,
					});
				})
				.catch((err) => {
					console.log(err);
				});
		});
	} else if (request.message === "get_blogs") {
		browser.storage.local.get(["user_id"], (data) => {
			fetch(`${Constants.BACKEND_URL}/user/${data.user_id}/blog/all`, {
				method: "GET",
				headers: {
					"Content-Type": "application/json",
					Accept: "application/json",
				},
			})
				.then((response) => {
					return response.json();
				})
				.then((data) => {
					sendResponse({
						message: "success",
						blogs: data,
					});
					return;
				})
				.catch((err) => {
					console.log(err);
				});
		});
	} else if (request.message === "veloghelper-change_email") {
		browser.storage.local.get(["user_id"], (data) => {
			fetch(`${Constants.BACKEND_URL}/user/${data.user_id}/email`, {
				method: "PUT",
				headers: {
					"Content-Type": "application/json",
					Accept: "application/json",
				},
				data: JSON.stringify({
					email: request.payload,
				}),
			})
				.then((response) => {
					sendResponse({
						message: "success",
					});
					return;
				})
				.catch((err) => {
					console.log(err);
				});
		});
	} else if (request.message === "veloghelper-get_email") {
		browser.storage.local.get(["user_id"], (data) => {
			fetch(`${Constants.BACKEND_URL}/user/${data.user_id}`, {
				method: "GET",
				headers: {
					"Content-Type": "application/json",
					Accept: "application/json",
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
				})
				.catch((err) => {
					console.log(err);
				});
		});
	} else if (request.message === "veloghelper-get_followers") {
		fetch(`${Constants.BACKEND_URL}/blog/${request.payload}/followers`, {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				Accept: "application/json",
			},
		})
			.then((response) => {
				return response.json();
			})
			.then((data) => {
				sendResponse({
					message: "success",
					followers: data,
				});
				return;
			})
			.catch((err) => {
				console.log(err);
			});
	}
	return true;
});
