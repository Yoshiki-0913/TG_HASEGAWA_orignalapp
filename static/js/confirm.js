// let card;
// document.addEventListener('DOMContentLoaded', async function () {
//   // Square Web Payments SDKの初期化
//   const payments = Square.payments("sandbox-sq0idb-I-uo9lQsYWtltYrCGQpuYg", "L0VHMSZC0YAWW");

//   try {
//     // カード要素を初期化
//     card = await payments.card();
//     await card.attach('#card-container'); // カード情報入力用のHTML要素にアタッチ
//   } catch (e) {
//     console.error('Payment initialization failed:', e);
//     return;
//   }

//   // ボタンクリックでトークンを取得
//   const cardButton = document.getElementById('card-button');
//   cardButton.addEventListener('click', async (event) => {
//     event.preventDefault();
//     const totalAmountText = document.getElementById('total-amount').innerText; // "合計： 800円" のような文字列を取得
//     const totalAmount = parseFloat(totalAmountText.match(/\d+/)[0]);
//     try {
//       const result = await card.tokenize();
//       if (result.status === 'OK') {
//         const nonce = result.token;

//         // サーバーに送信
//         const response = await fetch('/process_payment/', {
//           method: 'POST',
//           headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': '{{ csrf_token }}', // DjangoのCSRFトークン
//           },
//           body: JSON.stringify({
//             amount: totalAmount, // 合計金額
//             nonce: nonce, // Squareトークン
//           }),
//         });

//         const data = await response.json();
//         if (data.status === 'success') {
//           alert('支払いが成功しました！');
//         } else {
//           alert('エラーが発生しました: ' + data.message);
//         }
//       } else {
//         console.error(result.errors);
//         alert('支払いトークンの生成に失敗しました。詳細を確認してください。');
//       }
//     } catch (error) {
//       console.error('Tokenization failed:', error);
//       alert('トークン生成中にエラーが発生しました。');
//     }
//   });
// });