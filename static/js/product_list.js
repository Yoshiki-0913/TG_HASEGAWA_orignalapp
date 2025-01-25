// 商品の数量が変更されたときに合計金額を計算する
function updateTotalPrice() {
  let totalPrice = 0;

  // すべての商品を取得
  const productCards = document.querySelectorAll('.product-card');

  productCards.forEach(card => {
      const quantityInput = card.querySelector('input[type="text"]'); // 数量
      const priceElement = card.querySelector('.product-price'); // 商品価格の要素
      const quantity = parseInt(quantityInput.value); // 数量を取得
      const price = parseInt(priceElement.dataset.price); // データ属性から価格を取得

      totalPrice += quantity * price * 1.1; // 合計金額を計算
  });

  // 合計金額を表示
  const totalElement = document.getElementById('total-price');
  totalElement.textContent = `合計金額: ${Math.floor(totalPrice)}円(税込み)`;
}

// 増加ボタンが押されたとき
function increaseQuantity(id) {
  const quantityInput = document.getElementById(id);
  let currentValue = parseInt(quantityInput.value);
  quantityInput.value = currentValue + 1;
  updateTotalPrice(); // 合計金額を更新
}

// 減少ボタンが押されたとき
function decreaseQuantity(id) {
  const quantityInput = document.getElementById(id);
  let currentValue = parseInt(quantityInput.value);
  if (currentValue > 0) {
      quantityInput.value = currentValue - 1;
  }
  updateTotalPrice(); // 合計金額を更新
}

document.addEventListener('DOMContentLoaded', () => {
  const settlementSubmitButton = document.getElementById('settlement-submit');
  const settlementForm = document.getElementById('settlement-form');
  const settlementMethod = document.getElementById('settlement-method');
  const employeeName = '1';

  settlementSubmitButton.addEventListener('click', () => {
      const selectedMethod = settlementMethod.value;

      if (selectedMethod === 'cash') {
          const confirmation = confirm('決済確定します。よろしいですか？');
          if (confirmation) {
              // 現金決済用のデータを収集
              const total_price_text = document.getElementById('total-price').innerText; // 合計金額
              const total_price = total_price_text.match(/\d+/)[0];
              console.log("Total Price:", total_price);
              const selectedProducts = [];

              document.querySelectorAll('.product-card').forEach((card) => {
                  const productId = card.dataset.productId;
                  const quantity = card.querySelector('.quantity-input').value;
                  if (quantity > 0) {
                      selectedProducts.push([productId, quantity]);
                  }
              });

              // サーバーへデータを送信
              fetch('/handle_cash_settlement/', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                      'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                  },
                  body: JSON.stringify({
                      employee: employeeName,
                      settlement_amount: parseFloat(total_price).toFixed(2),
                      settlement_method: selectedMethod,
                      selected_products: selectedProducts,
                  }),
              })
              .then((response) => response.json())
              .then((data) => {
                  if (data.status === 'success') {
                      alert(data.message);
                      window.location.href = '/'; // 元のページへ戻る
                  } else {
                      alert(`エラー: ${data.message}`);
                  }
              });
              console.log("Total Price:2", total_price);

          }
      } else if (selectedMethod === 'card') {
          settlementForm.submit(); // カード決済は通常のフォーム送信
      } else {
          alert('決済方法を選択してください。');
      }
  });
});