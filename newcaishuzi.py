<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>猜数字游戏</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #fff;
  }
  .card {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 40px 50px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.2);
    width: 400px;
  }
  h1 { margin-bottom: 10px; font-size: 28px; }
  .range { margin-bottom: 20px; opacity: 0.85; font-size: 14px; }
  input[type="number"] {
    width: 100%;
    padding: 14px 18px;
    font-size: 20px;
    border: none;
    border-radius: 12px;
    text-align: center;
    outline: none;
    margin-bottom: 12px;
    background: rgba(255, 255, 255, 0.9);
    color: #333;
  }
  input[type="number"]:focus { box-shadow: 0 0 0 3px rgba(255,255,255,0.5); }
  button {
    width: 100%;
    padding: 14px;
    font-size: 16px;
    font-weight: 600;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    background: #fff;
    color: #764ba2;
    transition: transform 0.15s, box-shadow 0.15s;
  }
  button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.2); }
  button:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
  .feedback {
    margin: 20px 0 10px;
    min-height: 30px;
    font-size: 18px;
    font-weight: 600;
  }
  .feedback.high { color: #ffb4a2; }
  .feedback.low { color: #a2d2ff; }
  .feedback.win { color: #b5ead7; font-size: 22px; }
  .stats { margin-top: 15px; font-size: 14px; opacity: 0.85; }
  .history {
    margin-top: 20px;
    max-height: 120px;
    overflow-y: auto;
    font-size: 13px;
    text-align: left;
    background: rgba(0,0,0,0.1);
    border-radius: 10px;
    padding: 10px 14px;
  }
  .history p { padding: 3px 0; border-bottom: 1px solid rgba(255,255,255,0.1); }
  .history p:last-child { border-bottom: none; }
  .restart { margin-top: 12px; background: transparent; color: #fff; border: 2px solid #fff; }
  .restart:hover { background: rgba(255,255,255,0.2); color: #fff; }
</style>
</head>
<body>
  <div class="card">
    <h1>🎯 猜数字游戏</h1>
    <p class="range">我已经想好了一个 1 到 100 之间的数字</p>
    <input type="number" id="guess" placeholder="输入你的猜测" min="1" max="100" autocomplete="off">
    <button id="submitBtn" onclick="checkGuess()">猜一猜</button>
    <div class="feedback" id="feedback"></div>
    <div class="stats">已猜次数：<span id="attempts">0</span> / 剩余机会：<span id="remaining">10</span></div>
    <div class="history" id="history"></div>
    <button class="restart" onclick="initGame()" id="restartBtn" style="display:none;">再来一局</button>
  </div>

<script>
  let target, attempts, maxAttempts, gameOver;

  function initGame() {
    target = Math.floor(Math.random() * 100) + 1;
    attempts = 0;
    maxAttempts = 10;
    gameOver = false;
    document.getElementById('guess').value = '';
    document.getElementById('guess').disabled = false;
    document.getElementById('submitBtn').disabled = false;
    document.getElementById('restartBtn').style.display = 'none';
    document.getElementById('feedback').textContent = '';
    document.getElementById('feedback').className = 'feedback';
    document.getElementById('history').innerHTML = '';
    updateStats();
    document.getElementById('guess').focus();
    console.log('答案（调试用）：', target);
  }

  function updateStats() {
    document.getElementById('attempts').textContent = attempts;
    document.getElementById('remaining').textContent = maxAttempts - attempts;
  }

  function addHistory(guess, msg) {
    const p = document.createElement('p');
    p.textContent = `第 ${attempts} 次：${guess} → ${msg}`;
    const history = document.getElementById('history');
    history.insertBefore(p, history.firstChild);
  }

  function checkGuess() {
    if (gameOver) return;
    const input = document.getElementById('guess');
    const val = parseInt(input.value, 10);
    if (isNaN(val) || val < 1 || val > 100) {
      document.getElementById('feedback').textContent = '请输入 1 到 100 之间的数字！';
      document.getElementById('feedback').className = 'feedback high';
      return;
    }
    attempts++;
    updateStats();
    input.value = '';
    input.focus();

    const fb = document.getElementById('feedback');

    if (val === target) {
      fb.textContent = `🎉 恭喜！就是 ${target}，你用了 ${attempts} 次猜到！`;
      fb.className = 'feedback win';
      addHistory(val, '猜中了 🎉');
      endGame();
    } else if (val > target) {
      fb.textContent = '📉 大了，再小一点！';
      fb.className = 'feedback high';
      addHistory(val, '大了');
    } else {
      fb.textContent = '📈 小了，再大一点！';
      fb.className = 'feedback low';
      addHistory(val, '小了');
    }

    if (!gameOver && attempts >= maxAttempts && val !== target) {
      fb.textContent = `😢 机会用完了！正确答案是 ${target}。`;
      fb.className = 'feedback high';
      endGame();
    }
  }

  function endGame() {
    gameOver = true;
    document.getElementById('guess').disabled = true;
    document.getElementById('submitBtn').disabled = true;
    document.getElementById('restartBtn').style.display = 'block';
  }

  document.getElementById('guess').addEventListener('keydown', e => {
    if (e.key === 'Enter') checkGuess();
  });

  initGame();
</script>
</body>
</html>
