// make gray mark of processing state
function markProcessing (schemaID) {

  // console.log('markProcessing', '#'+'status'+schemaID);

  $('#'+'status'+schemaID).attr("class","btn btn-secondary");
};
// make green mark of ready state and put download link
function markDone (schemaID, task_result) {
  $('#'+'status'+schemaID).attr("class","btn btn-success");
  $('#'+'download'+schemaID).attr("href", task_result);
  $('#'+'download'+schemaID).attr("style","visibility: block");
};

var tasksDir = {};

$('.generate').on('click', function() {
  var quantity = $('#quantity').val();
  var userId = $('.userId').html();

  if (quantity == '') {
    // gentle reminder to enter quantity
    $('#quantity').attr('placeholder', 'How much?');
    return false;
  }
  // start tasks and get tasks ids
  $.ajax({
    // url: '/tasks/',
    url: 'tasks/',
    data: {
      userId: userId ,
      quantity: quantity ,
    },
    method: 'POST',
  })
  .done((tasksDict) => {
    for (const tsk in tasksDict) {

      console.log('res.task_id . done', tasksDict[tsk]);

      markProcessing(tsk);
      getStatus(tasksDict[tsk], tsk);

    }
  })
  .fail((err) => {

    console.log('res.task_id . err', err);

  });
});

function getStatus(taskId, schemaId) {

  console.log('getStatus(taskID, schemaId): ', taskId, schemaId)

  $.ajax({
    url: `tasks/${taskId}/`,
    method: 'GET'
  })
  .done((res) => {
    const html = `
      <tr>
        <td>${res.task_id}</td>
        <td>${res.task_status}</td>
        <td>${res.task_result}</td>
      </tr>`
    $('#tasks').prepend(html);

    // console.log('res.task_result: ', res.task_result);

    const taskStatus = res.task_status;
    const task_result = res.task_result;
    if (taskStatus === 'SUCCESS') {
      markDone(schemaId, task_result);
    };
    if (taskStatus === 'SUCCESS' || taskStatus === 'FAILURE') return false;
    setTimeout(function() {
      getStatus(taskId, schemaId);
    }, 500);
  })
  .fail((err) => {
    console.log(err)
  });
}