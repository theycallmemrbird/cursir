const card = document.querySelector("#card");
const cardId = document.querySelector("#card-id");
const cardCategory = document.querySelector("#card-category");
const cardTone = document.querySelector("#card-tone");
const cardText = document.querySelector("#card-text");
const message = document.querySelector("#message");
const remainingCount = document.querySelector("#remaining-count");
const totalCount = document.querySelector("#total-count");
const drawButton = document.querySelector("#draw-button");
const resetButton = document.querySelector("#reset-button");

let isDrawing = false;

function updateCounts(remaining, total) {
  remainingCount.textContent = remaining;
  totalCount.textContent = total;
}

function showCard(drawnCard) {
  card.classList.remove("card-empty");
  cardId.textContent = `#${drawnCard.id}`;
  cardCategory.textContent = drawnCard.category;
  cardTone.textContent = drawnCard.tone;
  cardText.textContent = drawnCard.text;
}

function showEmptyDeck() {
  card.classList.add("card-empty");
  cardId.textContent = "Empty";
  cardCategory.textContent = "Refresh needed";
  cardTone.textContent = "No cards remaining";
  cardText.textContent = "Refresh the deck to put every card back in play.";
}

async function drawCard() {
  if (isDrawing) {
    return;
  }

  isDrawing = true;
  drawButton.disabled = true;
  message.textContent = "";

  try {
    const response = await fetch("/draw", { method: "POST" });
    if (!response.ok) {
      throw new Error("Unable to draw a card.");
    }

    const payload = await response.json();
    updateCounts(payload.remaining, payload.total);

    if (payload.card) {
      showCard(payload.card);
    } else {
      showEmptyDeck();
      message.textContent = payload.message;
    }
  } catch (error) {
    message.textContent = error.message;
  } finally {
    drawButton.disabled = false;
    isDrawing = false;
  }
}

async function resetDeck() {
  resetButton.disabled = true;
  message.textContent = "";

  try {
    const response = await fetch("/reset", { method: "POST" });
    if (!response.ok) {
      throw new Error("Unable to refresh the deck.");
    }

    const payload = await response.json();
    updateCounts(payload.remaining, payload.total);
    card.classList.add("card-empty");
    cardId.textContent = "Ready";
    cardCategory.textContent = "Deck refreshed";
    cardTone.textContent = "Spacebar or Draw Card";
    cardText.textContent = "All cards are back in the deck.";
    message.textContent = payload.message;
  } catch (error) {
    message.textContent = error.message;
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

  const activeElement = document.activeElement;
  const isTyping =
    activeElement &&
    ["INPUT", "TEXTAREA", "SELECT", "BUTTON"].includes(activeElement.tagName);

  if (isTyping) {
    return;
  }

  event.preventDefault();
  drawCard();
});
