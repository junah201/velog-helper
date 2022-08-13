const Constants = {
  BACKEND_URL: "http://127.0.0.1:8000",
};

async function getCurrentTab() {
  let queryOptions = { active: true, lastFocusedWindow: true };
  // `tab` will either be a `tabs.Tab` instance or `undefined`.
  let [tab] = await chrome.tabs.query(queryOptions);
  return tab;
}

chrome.runtime.onInstalled.addListener(() => {
  chrome.identity.getProfileUserInfo(function (userInfo) {
    // 로그인 되어 있지 않은 유저일 경우
    if (userInfo.email === "") {
      // TODO: 모르겠다 나중에 개발해야지
    }
    // 로그인 되어 있는 유저 일 경우
    else {
      console.log(userInfo);
      chrome.storage.local.set({
        user_id: userInfo.id,
        user_email: userInfo.email,
      });
    }
    // 백엔드에 유저 등록
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
  });
});

async function onUpdated(tabId) {
  const tab = await chrome.tabs.get(tabId);
  console.log(tab);
  if (tab.status == "complete" && /^http/.test(tab.url)) {
    console.log(123132);
    chrome.scripting
      .insertCSS({
        target: { tabId: tab.id },
        files: ["./src/notice.css"],
      })
      .then(() => {
        chrome.scripting
          .executeScript({
            target: { tabId: tab.id },
            files: ["./src/notice.js"],
          })
          .then(() => {
            console.log("SUCCES add notice button");
          });
      })
      .catch((err) => console.log(err));
  }
  // 개인 블로그 메인 페이지 라면?
  if (
    tab.status == "complete" &&
    /^http/.test(tab.url) &&
    tab.url.split("/").slice(-1) != "" &&
    tab.url.split("/").length === 4
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
            files: ["./src/bookmark.js"],
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
          return response.json();
        })
        .then((data) => {
          sendResponse({ message: "success", data: data.archive });
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
