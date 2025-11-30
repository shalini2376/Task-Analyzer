const analyzeBtn = document.getElementById("analyzeBtn")
const suggestBtn = document.getElementById("suggestBtn")
const taskInput = document.getElementById("taskInput")
const resultsDiv = document.getElementById("results")
const sortingStrategySelect = document.getElementById("sortingStrategy")

const API_BASE = "http://127.0.0.1:8000/api/tasks"


function safeParseJSON(inputText) {
  try {
    const parsed = JSON.parse(inputText)
    if (!Array.isArray(parsed)) {
      alert("JSON must be an array of task objects.")
      return null
    }
    return parsed
  } catch (e) {
    alert("Invalid JSON. Please check your input.")
    return null
  }
}


function getPriorityClass(score) {
  if (score >= 140) return "priority-high"
  if (score >= 100) return "priority-medium"
  return "priority-low"
}


function applySortingStrategy(tasks, strategy) {
  // We already receive scored tasks from backend.
  // Here we allow user to view them with different perspectives.
  const cloned = [...tasks]

  if (strategy === "fastest") {
    cloned.sort((a, b) => {
      const ah = Number(a.estimated_hours) || 0
      const bh = Number(b.estimated_hours) || 0
      return ah - bh
    })
  } else if (strategy === "deadline") {
    cloned.sort((a, b) => {
      const ad = new Date(a.due_date)
      const bd = new Date(b.due_date)
      return ad - bd
    })
  } else {
    // default: sort by score (already sorted in backend, but we can ensure)
    cloned.sort((a, b) => (b.score || 0) - (a.score || 0))
  }

  return cloned
}


function renderTasks(tasks) {
  resultsDiv.innerHTML = ""

  if (!tasks || tasks.length === 0) {
    const msg = document.createElement("p")
    msg.className = "empty-state"
    msg.textContent = "No tasks to display. Paste some JSON and click Analyze."
    resultsDiv.appendChild(msg)
    return
  }

  const strategy = sortingStrategySelect.value
  const sortedTasks = applySortingStrategy(tasks, strategy)

  sortedTasks.forEach(task => {
    const card = document.createElement("div")
    const score = task.score || 0
    const priorityClass = getPriorityClass(score)

    card.className = `task-card ${priorityClass}`

    const header = document.createElement("div")
    header.className = "task-header"

    const titleEl = document.createElement("div")
    titleEl.className = "task-title"
    titleEl.textContent = task.title || "(Untitled Task)"

    const scoreEl = document.createElement("div")
    scoreEl.className = "task-score"
    scoreEl.textContent = `Score: ${score}`

    header.appendChild(titleEl)
    header.appendChild(scoreEl)

    const meta = document.createElement("div")
    meta.className = "task-meta"
    meta.textContent = `Due: ${task.due_date || "N/A"} • Importance: ${task.importance ?? "N/A"} • Hours: ${task.estimated_hours ?? "N/A"}`

    const explanation = document.createElement("div")
    explanation.className = "task-explanation"
    explanation.textContent = task.explanation || "No explanation available. (Use Suggest to generate explanations.)"

    card.appendChild(header)
    card.appendChild(meta)
    card.appendChild(explanation)

    resultsDiv.appendChild(card)
  })
}


async function analyzeTasks() {
  const rawInput = taskInput.value.trim()
  const tasks = safeParseJSON(rawInput)
  if (!tasks) return

  try {
    const response = await fetch(`${API_BASE}/analyze/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(tasks),
    })

    if (!response.ok) {
      const errorData = await response.json()
      alert(`Error: ${errorData.error || "Failed to analyze tasks"}`)
      return
    }

    const sortedTasks = await response.json()
    renderTasks(sortedTasks)
  } catch (error) {
    console.error("Analyze error:", error)
    alert("Failed to reach backend. Is the Django server running?")
  }
}


async function suggestTasks() {
  const rawInput = taskInput.value.trim()
  const tasks = safeParseJSON(rawInput)
  if (!tasks) return

  try {
    const response = await fetch(`${API_BASE}/suggest/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(tasks),
    })

    if (!response.ok) {
      const errorData = await response.json()
      alert(`Error: ${errorData.error || "Failed to suggest tasks"}`)
      return
    }

    const suggested = await response.json()
    renderTasks(suggested)
  } catch (error) {
    console.error("Suggest error:", error)
    alert("Failed to reach backend. Is the Django server running?")
  }
}


analyzeBtn.addEventListener("click", analyzeTasks)
suggestBtn.addEventListener("click", suggestTasks)
sortingStrategySelect.addEventListener("change", () => {
  // Re-render with new strategy if tasks already exist
  const cardsExist = resultsDiv.children.length > 0
  if (!cardsExist) return

  // Quick hack: store last response? For now, we simply ask user to click Analyze again.
  // But to be nicer, you could store the last tasks globally.
})
