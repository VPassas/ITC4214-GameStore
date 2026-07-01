// Handles AJAX rating and liking on a game's detail page.

const actions = document.querySelector("#game-actions");

// only run if the action box is on the page for logged in users only
if (actions) {
  const rateUrl = actions.dataset.rateUrl;
  const likeUrl = actions.dataset.likeUrl;
  const csrf = actions.dataset.csrf;
  let liked = actions.dataset.liked === "true";

  const stars = actions.querySelectorAll(".star");
  const likeBtn = actions.querySelector("#like-btn");

  // fill stars up to `score`, empty the rest
  function paintStars(score) {
    stars.forEach((star) => {
      const value = Number(star.dataset.score);
      star.textContent = value <= score ? "★" : "☆";
      star.classList.toggle("text-warning", value <= score);
    });
  }

  // show whether the game is currently liked
  function paintLike() {
    likeBtn.textContent = liked ? "♥ Liked" : "Like";
    likeBtn.classList.toggle("btn-danger", liked);
    likeBtn.classList.toggle("btn-outline-danger", !liked);
  }

  // this is created so we do not repeat the fetch setup for rate and like
  function postData(url, body) {
    return fetch(url, {
      method: "POST",
      headers: { "X-CSRFToken": csrf },
      body: body,
    }).then((response) => response.json());
  }

  // paint the stars and the like of the user's current state on page load
  paintStars(Number(actions.dataset.userScore));
  paintLike();

  // clicking a star sends the score and updates the average
  stars.forEach((star) => {
    star.addEventListener("click", () => {
      const score = star.dataset.score;
      postData(rateUrl, new URLSearchParams({ score: score })).then((data) => {
        if (data.error) {
          return;
        }
        paintStars(data.user_score);
        document.querySelector("#avg").textContent = data.average;
        document.querySelector("#rating-count").textContent = data.count;
      });
    });
  });

  // clicking like toggles it and updates the count
  likeBtn.addEventListener("click", () => {
    postData(likeUrl, new URLSearchParams()).then((data) => {
      liked = data.liked;
      paintLike();
      document.querySelector("#like-count").textContent = data.count;
    });
  });
}
