// =============================================================
//  form-handler.js  —  Student Registration
//  Plain JavaScript — works directly in index.html
// =============================================================

(function () {
  'use strict';

  const form      = document.getElementById('studentForm');
  const nameEl    = document.getElementById('name');
  const emailEl   = document.getElementById('email');
  const courseEl  = document.getElementById('course');
  const termsEl   = document.getElementById('terms');
  const submitBtn = document.getElementById('submitBtn');
  const btnText   = document.getElementById('buttonText');
  const spinner   = document.getElementById('spinner');
  const messageEl = document.getElementById('message');

  // ── Enable / disable button based on checkbox ─────────────
  termsEl.addEventListener('change', () => {
    submitBtn.disabled = !termsEl.checked;
  });

  // ── Form submit ───────────────────────────────────────────
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    messageEl.textContent = '';
    messageEl.style.color = '';

    const payload = {
      name:   nameEl.value.trim(),
      email:  emailEl.value.trim(),
      course: courseEl.value.trim(),
    };

    // Client-side validation
    if (!payload.name) {
      showMessage('Please enter your name.', 'red');
      nameEl.focus();
      return;
    }
    if (!payload.email) {
      showMessage('Please enter your email.', 'red');
      emailEl.focus();
      return;
    }
    if (!payload.course) {
      showMessage('Please enter your course.', 'red');
      courseEl.focus();
      return;
    }

    // Set loading state
    setLoading(true);

    try {
      const response = await fetch('/submit', {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify(payload),
      });

      const result = await response.json();

      if (response.ok) {
        showMessage(result.message || 'Registered successfully!', 'green');
        form.reset();
        submitBtn.disabled = true;
      } else {
        showMessage(result.message || 'Something went wrong. Please try again.', 'red');
      }

    } catch (err) {
      console.error(err);
      showMessage('Network error. Please check your connection and try again.', 'red');
    }

    setLoading(false);
  });

  // ── Helpers ───────────────────────────────────────────────
  function setLoading(isLoading) {
    submitBtn.disabled  = isLoading;
    btnText.textContent = isLoading ? 'Submitting...' : 'Register';
    spinner.classList.toggle('hidden', !isLoading);
  }

  function showMessage(text, color) {
    messageEl.textContent = text;
    messageEl.style.color = color;
  }

})();