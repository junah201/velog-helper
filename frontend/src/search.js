function createSearchResultItem(result) {
	var item = createElement("div", {
		class: "sc-TBWPX fmDHbD",
	});

	var thumbnail = createElement("a", {
		href: result.thumbnail_link,
	});

	var thumbnailImgContainer = createElement("div", {
		class: "sc-khQegj fQQSfY post-thumbnail",
		style: "padding-top: 52.356%;",
	});

	var thumbnailImg = createElement("img", {
		src: result.thumbnail_link,
		alt: "post-thumbnail",
	});

	thumbnailImgContainer.append(thumbnailImg);
	thumbnail.append(thumbnailImgContainer);

	var titleContainer = createElement("a", {
		href: result.link,
	});

	var title = createElement("h2", {});
	title.innerHTML = result.html_title;

	titleContainer.append(title);

	var snippet = createElement("p", {});
	snippet.innerHTML = result.html_snippet;

	item.append(thumbnail);
	item.append(titleContainer);
	item.append(snippet);

	return item;
}

function replaceSearchResults(query) {
	console.log(query);
	browser.runtime.sendMessage(
		{
			message: "get_search_results",
			payload: query,
		},
		(response) => {
			console.log(response);
			console.log(!!response);

			if (!response) {
				return;
			}

			var total = document.querySelector(
				"div.sc-hiwPVj.dezvna.sc-ehCJOs.bVUmaI > p.sc-faUpoM.ihDYHJ > b"
			);

			total.innerHTML = `${response.total}개`;

			var results = document.querySelector("div.sc-ZOtfp.cQfIhU");

			results.innerHTML = "";

			response.results.forEach((result) => {
				results.append(createSearchResultItem(result));
			});
		}
	);
}

var searchInput = document.querySelector("div > input");

if (searchInput) {
	searchInput.addEventListener("keyup", (e) => {
		if ((e.key = "Enter")) {
			replaceSearchResults(e.target.value);
		}
	});
}
