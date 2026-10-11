/**
 * Hangisini Seçersin? (Would You Rather?)
 * Asenkron Oylama (Fetch API) ve İnteraktif Deneyim
 */

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.addEventListener('DOMContentLoaded', () => {
  // CSRF Token
  const csrftoken = getCookie('csrftoken') || document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

  // Oylama Butonları Dinleyicisi
  document.querySelectorAll('.choice-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      const button = e.currentTarget;
      if (button.disabled) return;

      const choiceId = button.dataset.choiceId;
      const questionId = button.dataset.questionId;
      const card = button.closest('.dilemma-card') || button.closest('.focus-card') || button.closest('.feed-card');

      if (!choiceId || !card) return;

      // Aynı anda tekrar tıklanmasını önle
      const allButtonsInCard = card.querySelectorAll('.choice-btn');
      allButtonsInCard.forEach(b => b.disabled = true);
      button.style.opacity = '0.7';

      try {
        const response = await fetch(`/vote/${choiceId}/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
          }
        });

        const data = await response.json();
        button.style.opacity = '1';

        if (data.success) {
          // Sonuçları göster
          applyVoteResults(card, data, choiceId);

          // LocalStorage kaydı
          try {
            const votedSet = JSON.parse(localStorage.getItem('wyr_voted') || '[]');
            if (!votedSet.includes(parseInt(questionId))) {
              votedSet.push(parseInt(questionId));
              localStorage.setItem('wyr_voted', JSON.stringify(votedSet));
            }
          } catch (err) {}

          // Eğer focus modundaysak Sıradaki İkilem butonunu göster
          const nextWrapper = document.getElementById('focus-next-wrapper');
          if (nextWrapper) {
            nextWrapper.style.display = 'flex';
            nextWrapper.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
          }
        } else {
          alert(data.error || 'Bir hata oluştu.');
          allButtonsInCard.forEach(b => b.disabled = false);
        }
      } catch (err) {
        console.error('Oy verme hatası:', err);
        allButtonsInCard.forEach(b => b.disabled = false);
        button.style.opacity = '1';
      }
    });
  });

  // Oylama Sonuçlarını UI'ya Uygulama Fonksiyonu
  function applyVoteResults(card, data, chosenChoiceId) {
    const choiceBoxes = card.querySelectorAll('.choice-box');
    
    // Butonları devre dışı bırak ve seçileni işaretle
    choiceBoxes.forEach(box => {
      const btn = box.querySelector('.choice-btn');
      btn.disabled = true;

      if (btn.dataset.choiceId == (data.chosen_id || chosenChoiceId)) {
        if (!box.querySelector('.choice-voted-badge')) {
          const badge = document.createElement('span');
          badge.className = 'choice-voted-badge';
          badge.textContent = '✓ Senin Tercihin';
          box.appendChild(badge);
        }
      }

      // Sonuç kapsayıcısını aç
      const resultBox = box.querySelector('.result-container');
      if (resultBox) {
        resultBox.classList.add('show');
      }
    });

    // A ve B seçeneklerinin progress barlarını doldur
    const fillA = card.querySelector('.fill-a');
    const fillB = card.querySelector('.fill-b');
    const pctA = card.querySelector('.pct-a-text');
    const pctB = card.querySelector('.pct-b-text');
    const votesA = card.querySelector('.votes-a-text');
    const votesB = card.querySelector('.votes-b-text');
    const totalVotes = card.querySelector('.total-votes-text');

    if (pctA) pctA.textContent = `%${data.pct_a}`;
    if (pctB) pctB.textContent = `%${data.pct_b}`;
    if (votesA) votesA.textContent = `${data.votes_a} oy`;
    if (votesB) votesB.textContent = `${data.votes_b} oy`;
    if (totalVotes) totalVotes.textContent = `${data.total_votes} oy`;

    // Akıcı animasyonla barı doldur
    setTimeout(() => {
      if (fillA) fillA.style.width = `${data.pct_a}%`;
      if (fillB) fillB.style.width = `${data.pct_b}%`;
    }, 50);

    // Son oy verenleri güncelle
    if (data.recent_voters && data.recent_voters.length > 0) {
      const votersList = card.querySelector('.voters-list');
      if (votersList) {
        votersList.innerHTML = data.recent_voters.map(u => `<span class="voter-pill">@${u}</span>`).join('');
      }
    }
  }

  // Profil Sekmeleri (Tabs)
  const tabBtns = document.querySelectorAll('.tab-btn');
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const target = document.getElementById(btn.dataset.tab);
      if (target) target.classList.add('active');
    });
  });

  // Otomatik Kapanan Bildirimler (Toasts)
  const alerts = document.querySelectorAll('.alert');
  if (alerts.length > 0) {
    setTimeout(() => {
      alerts.forEach(a => {
        a.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        a.style.opacity = '0';
        a.style.transform = 'translateY(-10px)';
        setTimeout(() => a.remove(), 500);
      });
    }, 4000);
  }
});
