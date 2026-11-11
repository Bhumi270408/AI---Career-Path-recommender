const featureIds = ["python","coding","math","communication","creativity","problem_solving","tech_interest","business_interest","design_interest","helping_interest"];

featureIds.forEach(id => {
  const slider = document.getElementById(id);
  const output = document.getElementById(`${id}-value`);
  slider.addEventListener("input", () => output.textContent = Number(slider.value).toFixed(1).replace(".0",""));
});

const button = document.getElementById("recommend-btn");
const resultsSection = document.getElementById("results");
const resultsContainer = document.getElementById("recommendations");
const disclaimer = document.getElementById("disclaimer");

button.addEventListener("click", async () => {
  const values = {};
  featureIds.forEach(id => values[id] = Number(document.getElementById(id).value));
  button.disabled = true;
  button.querySelector("span").textContent = "Finding your matches...";
  try {
    const response = await fetch("/recommend", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify(values)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Something went wrong.");
    resultsContainer.innerHTML = data.recommendations.map((item, index) => `
      <article class="career-card">
        <div class="career-rank">MATCH ${String(index+1).padStart(2,"0")}</div>
        <h3>${escapeHtml(item.career)}</h3>
        <div class="match-caption"><span>Profile match</span><b>${item.match}%</b></div>
        <div class="match-line"><div class="match-fill" style="width:${Math.max(3,item.match)}%"></div></div>
        <p>${escapeHtml(item.summary)}</p>
        <h4>Strengths to build on</h4>
        <div>${item.strengths.length ? item.strengths.map(x=>`<span class="tag">${escapeHtml(x)}</span>`).join("") : '<span class="tag">Keep exploring</span>'}</div>
        <h4>Skills to develop</h4>
        <div>${item.gaps.length ? item.gaps.map(x=>`<span class="tag gap-tag">${escapeHtml(x.skill)} · ${x.current}/5</span>`).join("") : '<span class="tag">Great starting alignment</span>'}</div>
        <h4>Starter roadmap</h4>
        <ol class="roadmap">${item.roadmap.map(x=>`<li>${escapeHtml(x)}</li>`).join("")}</ol>
        <h4>Possible entry roles</h4>
        <div>${item.roles.map(x=>`<span class="tag">${escapeHtml(x)}</span>`).join("")}</div>
      </article>
    `).join("");
    disclaimer.textContent = data.note;
    resultsSection.classList.remove("hidden");
    resultsSection.scrollIntoView({behavior:"smooth", block:"start"});
  } catch (error) {
    alert(error.message);
  } finally {
    button.disabled = false;
    button.querySelector("span").textContent = "Find my career paths";
  }
});

document.getElementById("reset-btn").addEventListener("click", () => {
  resultsSection.classList.add("hidden");
  document.querySelector(".workspace").scrollIntoView({behavior:"smooth"});
});

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, char => ({
    "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;"
  }[char]));
}
