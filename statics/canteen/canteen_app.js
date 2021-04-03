let student = document.getElementById('student');
let app = document.getElementById('app');
let lead = document.getElementById('lead')
let skip = document.getElementById('skip')

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie('csrftoken');
const jsonHeaders = new Headers({
  'Content-Type': 'application/json',
  'X-CSRFToken': csrftoken
})
app.addEventListener('click', (event) => {
  if (event.target.dataset.pk) {
    if (confirm('确认提交？')) {
      fetch('/canteen/askmeal', {
        method: 'POST',
        body: JSON.stringify({
          student: student.dataset.pk,
          foodForMeal: event.target.dataset.pk
        }),
        headers: jsonHeaders
      }).then((response) => {
        response.text().then((text) => {
          app.innerHTML = text;
          let data = JSON.parse(document.getElementById('data').dataset.json);
          if (data.success) {
            if (data.hasContent) {
              lead.innerText = `您现在点的餐是:${data.date}${data.description}`;
              lead.dataset.pk = data.meal_pk
            } else {
              lead.innerText = '暂无新的可点餐点!'
            }
          } else {
            alert(`错误!\nerror message:${data.error_message}`);
          }
        })
      })
    }
  }
}, false);
skip.addEventListener('click', (event) => {
  if (confirm('确认跳过本餐？')) {
    lead.innerText = '正在获取下一餐数据';
    fetch('/canteen/nextmeal', {
      method: 'POST',
      body: JSON.stringify({
        student: student.dataset.pk,
        meal_pk: lead.dataset.pk
      }),
      headers: jsonHeaders
    }).then((response) => {
      response.text().then((text) => {
        app.innerHTML = text;
        let data = JSON.parse(document.getElementById('data').dataset.json);
        if (data.hasContent) {
          lead.innerText = `您现在点的餐是:${data.date}${data.description}`;
          lead.dataset.pk = data.meal_pk
        } else {
          lead.innerText = '暂无新的可点餐点!';
        }
      })
    })
  }
})