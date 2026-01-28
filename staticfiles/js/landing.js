function createRandomStars() {
  const page = document.querySelector(".page");
  const starCount = 200; // Total stars

  for (let i = 0; i < starCount; i++) {
    const star = document.createElement("div");
    star.className = "star";

    // Random size distribution (more small stars, fewer large)
    const rand = Math.random();
    if (rand < 0.7) {
      star.classList.add("star-small");
    } else if (rand < 0.9) {
      star.classList.add("star-medium");
    } else {
      star.classList.add("star-large");
    }

    // 15% chance of purple accent star
    if (Math.random() < 0.3) {
      star.classList.add("star-purple");
    }

    // Completely random position
    star.style.left = Math.random() * 100 + "%";
    star.style.top = Math.random() * 100 + "%";

    // Random animation delay for varied twinkling
    star.style.animationDelay = Math.random() * 3 + "s";

    page.appendChild(star);
  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", createRandomStars);
} else {
  createRandomStars();
}
