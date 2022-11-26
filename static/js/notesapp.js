async function togglecomplete(subtask_id) {
    // Make the ajax request through JQuery
    $.ajax({
        // Send a get request to the given url
        url: '/tasks/togglecomplete',
        type: 'get',
        data: {
            // Using JSON to send the subtask id
            subtask_id: subtask_id,
        },
        // Run on a successful server response
        success: function (response) {
            
            if (response.complete == true) {
                // Toggle the class on the subtask
                $("#tid_" + response.tid).removeClass("incomplete");
                $("#tid_" + response.tid).addClass("complete");
            }
            else {
                // Toggle the class on the subtask
                $("#tid_" + response.tid).removeClass("complete");
                $("#tid_" + response.tid).addClass("incomplete");
            }
        }
    });
}

async function delete_t(subtask_id) {
    // Make the ajax request through JQuery
    $.ajax({
        url: '/tasks/deletesubtask',
        // Send a get request to the given url
        type: 'get',
        data: {
            // Using JSON to send the subtask id
            subtask_id: subtask_id,
        },
        // Run on a successful server response
        success: function (response) {
            if (response.delete_success == true) {
                // Hide the deleted subtask
                $("#tid_" + response.tid).hide();
            }
        }
    });
} 