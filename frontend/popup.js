const blogItmes = createBlogItems();
const noticeItems = createNoticeItems();
const settings = createSettings();

document.querySelector("main").append(blogItmes);
document.querySelector("main").append(noticeItems);
document.querySelector("main").append(settings);

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
