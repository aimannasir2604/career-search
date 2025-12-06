const quizQuestions = [
  {
    text: "How do you prefer to solve problems?",
    options: [
      { text: "Through logical analysis and data", trait: "analytical" },
      { text: "By thinking outside the box", trait: "creative" },
      { text: "Working with others to find solutions", trait: "social" },
      { text: "Using hands-on practical methods", trait: "practical" },
    ],
  },
  {
    text: "Which activity sounds most enjoyable to you?",
    options: [
      { text: "Designing or creating something new", trait: "creative" },
      { text: "Leading a team project", trait: "social" },
      { text: "Conducting experiments or research", trait: "analytical" },
      { text: "Fixing or building physical things", trait: "practical" },
    ],
  },
  {
    text: "In group projects, you usually:",
    options: [
      { text: "Organize tasks and keep everyone on track", trait: "social" },
      { text: "Come up with unique ideas and approaches", trait: "creative" },
      { text: "Handle the technical or detailed work", trait: "analytical" },
      { text: "Do the hands-on implementation", trait: "practical" },
    ],
  },
];

const totalQuestions = quizQuestions.length;

let currentIndex = 0;
let selectedTraitCounts = { analytical: 0, creative: 0, social: 0, practical: 0 };
let userAnswers = []; // Store user's answers for review
let timerSeconds = 0;
let quizCompleted = false;

function startQuizTimer() {
  const timeEl = document.getElementById("quiz-time");
  setInterval(() => {
    timerSeconds += 1;
    timeEl.textContent = `${timerSeconds}s`;
  }, 1000);
}

function renderQuestion() {
  const question = quizQuestions[currentIndex];
  const questionNumberEl = document.getElementById("quiz-question-number");
  const questionTextEl = document.getElementById("quiz-question-text");
  const optionsContainer = document.getElementById("quiz-options");
  const counterEl = document.getElementById("quiz-question-counter");
  const nextBtn = document.getElementById("quiz-next-btn");
  const progressFill = document.getElementById("quiz-progress-fill");
  const reviewSection = document.getElementById("quiz-review");
  const resultSection = document.getElementById("quiz-result");

  // Hide review and result sections when showing questions
  if (reviewSection) reviewSection.classList.add("hidden");
  if (resultSection) resultSection.classList.add("hidden");

  questionNumberEl.textContent = currentIndex + 1;
  questionTextEl.textContent = question.text;
  counterEl.textContent = `${currentIndex + 1}/${totalQuestions}`;

  const progress = ((currentIndex) / totalQuestions) * 100;
  progressFill.style.width = `${progress}%`;

  optionsContainer.innerHTML = "";
  nextBtn.disabled = true;
  nextBtn.textContent = currentIndex < totalQuestions - 1 ? "Next Question →" : "Finish Quiz →";

  // Check if user already answered this question
  const existingAnswer = userAnswers[currentIndex];

  question.options.forEach((opt, index) => {
    const btn = document.createElement("button");
    btn.className = "quiz-option-btn";
    btn.textContent = opt.text;
    btn.dataset.trait = opt.trait;
    
    // Pre-select if user already answered
    if (existingAnswer && existingAnswer.trait === opt.trait) {
      btn.classList.add("selected");
      nextBtn.disabled = false;
    }
    
    btn.addEventListener("click", () => {
      document
        .querySelectorAll(".quiz-option-btn")
        .forEach((b) => b.classList.remove("selected"));
      btn.classList.add("selected");
      nextBtn.disabled = false;
    });
    optionsContainer.appendChild(btn);
  });
}

function handleNextQuestion() {
  const selected = document.querySelector(".quiz-option-btn.selected");
  if (!selected) return;

  const trait = selected.dataset.trait;
  const questionText = quizQuestions[currentIndex].text;
  const selectedText = selected.textContent;

  // Store answer
  userAnswers[currentIndex] = {
    questionIndex: currentIndex,
    questionText: questionText,
    selectedText: selectedText,
    trait: trait
  };

  if (currentIndex < totalQuestions - 1) {
    currentIndex += 1;
    renderQuestion();
  } else {
    // All questions answered - show review section
    showReviewSection();
  }
}

function showReviewSection() {
  const reviewSection = document.getElementById("quiz-review");
  const nextBtn = document.getElementById("quiz-next-btn");
  const progressFill = document.getElementById("quiz-progress-fill");
  
  // Hide quiz question section
  document.querySelector(".quiz-question-box").style.display = "none";
  document.getElementById("quiz-options").style.display = "none";
  nextBtn.style.display = "none";
  
  // Update progress to 100%
  progressFill.style.width = "100%";
  
  // Show review section
  if (reviewSection) {
    reviewSection.classList.remove("hidden");
    
    // Populate review answers
    const reviewContainer = document.getElementById("quiz-review-answers");
    if (reviewContainer) {
      reviewContainer.innerHTML = "";
      
      userAnswers.forEach((answer, index) => {
        const reviewItem = document.createElement("div");
        reviewItem.className = "quiz-review-item";
        reviewItem.innerHTML = `
          <div class="quiz-review-question">
            <span class="quiz-review-qnum">Q${index + 1}:</span>
            <span class="quiz-review-qtext">${answer.questionText}</span>
          </div>
          <div class="quiz-review-answer">
            <strong>Your Answer:</strong> ${answer.selectedText}
          </div>
        `;
        reviewContainer.appendChild(reviewItem);
      });
    }
    
    // Scroll to review section
    setTimeout(() => {
      reviewSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 300);
  }
  
  quizCompleted = true;
}

function editAnswers() {
  // Reset to first question
  currentIndex = 0;
  
  // Show quiz question section again
  const questionBox = document.querySelector(".quiz-question-box");
  const optionsContainer = document.getElementById("quiz-options");
  const nextBtn = document.getElementById("quiz-next-btn");
  
  if (questionBox) questionBox.style.display = "block";
  if (optionsContainer) optionsContainer.style.display = "block";
  if (nextBtn) {
    nextBtn.style.display = "block";
    nextBtn.disabled = true;
  }
  
  // Hide review section
  const reviewSection = document.getElementById("quiz-review");
  if (reviewSection) {
    reviewSection.classList.add("hidden");
  }
  
  // Hide result section if visible
  const resultSection = document.getElementById("quiz-result");
  if (resultSection) {
    resultSection.classList.add("hidden");
  }
  
  // Re-render first question
  renderQuestion();
  
  // Scroll to top of quiz
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function calculateAndShowResults() {
  // Calculate trait counts from user answers
  selectedTraitCounts = { analytical: 0, creative: 0, social: 0, practical: 0 };
  userAnswers.forEach(answer => {
    selectedTraitCounts[answer.trait] += 1;
  });

  const progressFill = document.getElementById("quiz-progress-fill");
  progressFill.style.width = "100%";

  const resultEl = document.getElementById("quiz-result");
  const resultTextEl = document.getElementById("quiz-result-text");
  const reviewSection = document.getElementById("quiz-review");

  // Hide review section
  if (reviewSection) {
    reviewSection.classList.add("hidden");
  }

  let bestTrait = "analytical";
  let bestScore = -1;
  let totalAnswers = 0;
  Object.entries(selectedTraitCounts).forEach(([trait, count]) => {
    totalAnswers += count;
    if (count > bestScore) {
      bestScore = count;
      bestTrait = trait;
    }
  });

  const descriptions = {
    analytical:
      "You have a strong analytical personality. You enjoy working with data, logic, and structured problem-solving.",
    creative:
      "You are highly creative and imaginative. You like exploring new ideas, visuals, and ways to express yourself.",
    social:
      "You are people-focused and social. You gain energy from collaborating, communicating, and supporting others.",
    practical:
      "You are hands-on and practical. You prefer tangible tasks, real-world problem-solving, and making things work.",
  };

  resultTextEl.textContent = descriptions[bestTrait];

  // Update trait distribution bars
  const traitIds = ["analytical", "creative", "social", "practical"];
  traitIds.forEach((trait) => {
    const valueEl = document.getElementById(`trait-${trait}-value`);
    const barEl = document.getElementById(`trait-${trait}-bar`);
    const pct =
      totalAnswers > 0 ? Math.round((selectedTraitCounts[trait] / totalAnswers) * 100) : 0;
    if (valueEl) valueEl.textContent = `${pct}%`;
    if (barEl) barEl.style.width = `${pct}%`;
  });

  // Suggested careers based on dominant trait
  const careersByTrait = {
    analytical: [
      { title: "Data Analyst", desc: "Work with data to uncover patterns and support decisions." },
      { title: "Engineer", desc: "Design and improve systems, products, and technology." },
      { title: "Research Scientist", desc: "Investigate complex questions through experiments and analysis." },
      { title: "Financial Analyst", desc: "Analyze financial data to guide investments and planning." },
    ],
    creative: [
      { title: "Graphic Designer", desc: "Create visual concepts for brands, products, and media." },
      { title: "Content Creator", desc: "Produce engaging stories, videos, and digital content." },
      { title: "UX/UI Designer", desc: "Design user-friendly digital experiences and interfaces." },
      { title: "Marketing Specialist", desc: "Develop creative campaigns to reach and inspire audiences." },
    ],
    social: [
      { title: "Teacher", desc: "Support students’ growth through teaching and mentoring." },
      { title: "Counselor", desc: "Guide people through challenges with empathy and insight." },
      { title: "Human Resources", desc: "Help organizations support and develop their teams." },
      { title: "Social Worker", desc: "Advocate for and support individuals and communities." },
    ],
    practical: [
      { title: "Healthcare Professional", desc: "Provide hands-on care and support to patients." },
      { title: "Technician", desc: "Install, repair, and maintain technical systems or equipment." },
      { title: "Operations Manager", desc: "Keep day-to-day processes running smoothly." },
      { title: "Field Engineer", desc: "Work on-site to solve real-world technical problems." },
    ],
  };

  const cardsContainer = document.getElementById("quiz-career-cards");
  if (cardsContainer) {
    cardsContainer.innerHTML = "";
    (careersByTrait[bestTrait] || []).forEach((career) => {
      const card = document.createElement("div");
      card.className = "quiz-career-card";
      card.innerHTML = `<div class="quiz-career-title">${career.title}</div>
        <div class="quiz-career-desc">${career.desc}</div>`;
      cardsContainer.appendChild(card);
    });
  }

  resultEl.classList.remove("hidden");
  
  // Show submit button after results are displayed
  const submitBtn = document.getElementById("quiz-submit-btn");
  if (submitBtn) {
    submitBtn.style.display = "block";
    submitBtn.disabled = false;
    
    // Check if already submitted
    const isSubmitted = localStorage.getItem('quiz_submitted') === 'true';
    if (isSubmitted) {
      submitBtn.textContent = "✓ Submitted";
      submitBtn.style.background = "linear-gradient(135deg, #10b981, #059669)";
      submitBtn.disabled = true;
      
      const messageEl = document.getElementById("quiz-submit-message");
      if (messageEl) {
        messageEl.textContent = "✓ Quiz results already submitted!";
        messageEl.className = "quiz-submit-message success";
        messageEl.classList.remove("hidden");
      }
    }
  }
  
  // Scroll to results section
  setTimeout(() => {
    resultEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, 300);
}

function submitQuizResults() {
  const submitBtn = document.getElementById("quiz-submit-btn");
  const messageEl = document.getElementById("quiz-submit-message");
  
  if (!submitBtn || submitBtn.disabled) return;
  
  // Disable button to prevent double submission
  submitBtn.disabled = true;
  submitBtn.textContent = "Submitting...";
  
  // Calculate results
  let totalAnswers = 0;
  Object.values(selectedTraitCounts).forEach(count => {
    totalAnswers += count;
  });
  
  const results = {
    traits: {
      analytical: totalAnswers > 0 ? Math.round((selectedTraitCounts.analytical / totalAnswers) * 100) : 0,
      creative: totalAnswers > 0 ? Math.round((selectedTraitCounts.creative / totalAnswers) * 100) : 0,
      social: totalAnswers > 0 ? Math.round((selectedTraitCounts.social / totalAnswers) * 100) : 0,
      practical: totalAnswers > 0 ? Math.round((selectedTraitCounts.practical / totalAnswers) * 100) : 0,
    },
    time_taken: timerSeconds,
    total_questions: totalQuestions
  };
  
  // Determine dominant trait
  let bestTrait = "analytical";
  let bestScore = -1;
  Object.entries(selectedTraitCounts).forEach(([trait, count]) => {
    if (count > bestScore) {
      bestScore = count;
      bestTrait = trait;
    }
  });
  results.dominant_trait = bestTrait;
  
  // Save to localStorage and send to server
  try {
    localStorage.setItem('quiz_results', JSON.stringify(results));
    localStorage.setItem('quiz_submitted', 'true');
    localStorage.setItem('quiz_submitted_date', new Date().toISOString());
    
    // Send to server
    fetch('/api/quiz/submit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        analytical_score: results.traits.analytical,
        creative_score: results.traits.creative,
        social_score: results.traits.social,
        practical_score: results.traits.practical,
        dominant_trait: results.dominant_trait,
        time_taken: results.time_taken,
        total_questions: results.total_questions
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        // Show success message
        if (messageEl) {
          messageEl.textContent = "✓ Quiz results submitted successfully!";
          messageEl.className = "quiz-submit-message success";
          messageEl.classList.remove("hidden");
        }
        
        submitBtn.textContent = "✓ Submitted";
        submitBtn.style.background = "linear-gradient(135deg, #10b981, #059669)";
        
        // Scroll to message
        if (messageEl) {
          messageEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
      } else {
        throw new Error(data.error || 'Submission failed');
      }
    })
    .catch(error => {
      console.error('Error submitting to server:', error);
      // Still show success if localStorage worked
      if (messageEl) {
        messageEl.textContent = "✓ Quiz results saved locally!";
        messageEl.className = "quiz-submit-message success";
        messageEl.classList.remove("hidden");
      }
      submitBtn.textContent = "✓ Submitted";
      submitBtn.style.background = "linear-gradient(135deg, #10b981, #059669)";
    });
    
  } catch (error) {
    console.error('Error saving quiz results:', error);
    if (messageEl) {
      messageEl.textContent = "Error submitting results. Please try again.";
      messageEl.className = "quiz-submit-message error";
      messageEl.classList.remove("hidden");
    }
    submitBtn.disabled = false;
    submitBtn.textContent = "Submit Quiz Results";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const nextBtn = document.getElementById("quiz-next-btn");
  if (!nextBtn) return;
  nextBtn.addEventListener("click", handleNextQuestion);
  
  // Review section buttons
  const reviewEditBtn = document.getElementById("quiz-review-edit-btn");
  if (reviewEditBtn) {
    reviewEditBtn.addEventListener("click", editAnswers);
  }
  
  const reviewSubmitBtn = document.getElementById("quiz-submit-review-btn");
  if (reviewSubmitBtn) {
    reviewSubmitBtn.addEventListener("click", () => {
      // Calculate and show results
      calculateAndShowResults();
    });
  }
  
  // Add submit button event listener (for submitting results to server)
  const submitBtn = document.getElementById("quiz-submit-btn");
  if (submitBtn) {
    submitBtn.addEventListener("click", submitQuizResults);
    submitBtn.style.display = "none"; // Hide initially
    
    // Check if quiz was already submitted
    const isSubmitted = localStorage.getItem('quiz_submitted') === 'true';
    if (isSubmitted) {
      submitBtn.textContent = "✓ Submitted";
      submitBtn.style.background = "linear-gradient(135deg, #10b981, #059669)";
    }
  }
  
  startQuizTimer();
  renderQuestion();
});


