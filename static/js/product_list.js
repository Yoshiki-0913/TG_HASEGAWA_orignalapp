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
  totalElement.textContent = `${Math.floor(totalPrice)}`;
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
      } 
      else if (selectedMethod === 'card') 
      {
          const selectedProducts = [];
              // 各商品をループ
          document.querySelectorAll('.product-card').forEach(card => 
          {
            const productId = card.getAttribute('data-product-id');
            const productName = card.querySelector('.product-name').innerText;
            console.log("Name:", productName);
            const quantityInput = card.querySelector('.quantity-input');
            const quantity = parseInt(quantityInput.value, 10);
            const price = parseFloat(card.querySelector('.product-price').getAttribute('data-price'));
            if (quantity > 0) 
            {
              selectedProducts.push({
              id: productId,
              name: productName,
              quantity: quantity,
              price: price,});
            }
          });
          console.log(selectedProducts)

          // サーバーに送信（JSONデータ）
          fetch('/save_selection/', 
          {
            method: 'POST',
            headers: 
            {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify({ selectedProducts }),
          })
        .then(response => response.json())
        .then(data => 
        {
          if (data.status === 'success') 
            {
              window.location.href = '/confirm'; // 確認ページに遷移
            } 
            else 
            {
              alert('エラーが発生しました: ' + data.message);
            }
        })
        .catch(error => 
        {
          console.error('Error:', error);
          alert('送信中にエラーが発生しました。');
        });
      } 
      else
      {
          alert('決済方法を選択してください。');
      }
  });
});