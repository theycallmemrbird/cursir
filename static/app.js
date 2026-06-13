const card = document.querySelector("#card");
const cardId = document.querySelector("#card-id");
const cardTone = document.querySelector("#card-tone");
const cardCategory = document.querySelector("#card-category");
const cardText = document.querySelector("#card-text");
const deckMessage = document.querySelector("#deck-message");
const drawnCount = document.querySelector("#drawn-count");
const remainingCount = document.querySelector("#remaining-count");
const drawButton = document.querySelector("#draw-button");
const resetButton = document.querySelector("#reset-button");

let isDrawing = false;

async function postJson(url) {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  return response.json();
}

function updateCounts(data) {
  drawnCount.textContent = data.drawn;
  remainingCount.textContent = data.remaining;
}

function showCard(data) {
  updateCounts(data);

  if (!data.card) {
    card.classList.add("placeholder");
    cardId.textContent = "Deck empty";
    cardTone.textContent = "Refresh to reset";
    cardCategory.textContent = "No cards remaining";
    cardText.textContent = data.message || "Refresh the deck to draw again.";
    deckMessage.textContent = data.message || "The deck is empty.";
    return;
  }

  card.classList.remove("placeholder");
  cardId.textContent = `Card ${data.card.id}`;
  cardTone.textContent = data.card.tone;
  cardCategory.textContent = data.card.category;
  cardText.textContent = data.card.text;
  deckMessage.textContent = `${data.remaining} of ${data.total} cards remaining.`;
}

async function drawCard() {
  if (isDrawing) {
    return;
  }

  isDrawing = true;
  drawButton.disabled = true;
  deckMessage.textContent = "Drawing...";

  try {
    const data = await postJson("/api/draw");
    showCard(data);
  } catch (error) {
    deckMessage.textContent = "Something went wrong while drawing a card.";
  } finally {
    isDrawing = false;
    drawButton.disabled = false;
  }
}

async function resetDeck() {
  resetButton.disabled = true;

  try {
    const data = await postJson("/api/reset");
    updateCounts(data);
    card.classList.add("placeholder");
    cardId.textContent = "Ready";
    cardTone.textContent = "No card drawn yet";
    cardCategory.textContent = "Press Space";
    cardText.textContent = "Your next random card will appear here.";
    deckMessage.textContent = data.message;
  } catch (error) {
    deckMessage.textContent = "Something went wrong while refreshing the deck.";
  } finally {
    resetButton.disabled = false;
  }
}

drawButton.addEventListener("click", drawCard);
resetButton.addEventListener("click", resetDeck);

document.addEventListener("keydown", (event) => {
  if (event.code !== "Space" || event.repeat) {
    return;
  }

  const interactiveTags = ["BUTTON", "INPUT", "TEXTAREA", "SELECT", "A"];
  if (interactiveTags.includes(document.activeElement.tagName)) {
    return;
  }

  event.preventDefault();
  drawCard();
});
