var position_id = undefined;

function ajax_call({ url, type, data = [], msg, form_params = {}, call_back }) {
    if (form_params == true) {
        form_params = {
            processData: false,
            contentType: false,
            cache: false
        };
    }

    $.ajax({
        method: type,
        url: url,
        async: false,
        data: data,
        success: function(data, status = undefined) {
            if (call_back) {
                call_back(data);
            }

            if (status == 'success' && msg) {
                success_util(msg);
            }
        },
        error: function(xhr) {
            fail_util(xhr.responseJSON.message);
        },
        ...form_params
    });
}

function success_util(msg) {
    $.mSnackbar(msg);
    setTimeout(function() {
        $.mSnackbar().close();
    }, 2000);

    setTimeout(function() {
        location.reload();
    }, 1000);
}

function fail_util(msg) {
    $.mSnackbar(msg);
    setTimeout(function() {
        $.mSnackbar().close();
    }, 2000);
}

function getFormData(element) {
    let serialize_data = $(element).serializeArray();
    let data = {};
    $.map(serialize_data, function(n, i) {
        let val = n['value'];
        if (val.indexOf('[') > -1 & val.indexOf(']') > -1) {
            val = JSON.parse(val)
        }
        data[n['name']] = val;
    });
    return JSON.stringify(data);
}

function deletePosition(position_id) {
    $.confirm({
        icon: "fa fa-trash-alt",
        title: "DELETE",
        boxWidth: "30%",
        content: "Are you Sure you want to delete this record",
        theme: "dark",
        type: "red",
        // columnClass: 'col-md-4 col-md-offset-4',
        closeIcon: true,
        typeAnimated: true,
        buttons: {
            tryAgain: {
                text: "Ok",
                btnClass: "btn-red",
                action: function() {
                    let url = "/api/position/" + position_id + "/";
                    let type = "DELETE";
                    let msg = 'Deleted Successfully';
                    ajax_call({ url, type, msg });
                }
            },
            Close: function() {}
        }
    });
}

function submitForm(e) {
    let type, msg, url = undefined;
    if (position_id) {
        type = 'PUT'
        msg = 'Position Updated Successfully'
        url = "/api/position/" + position_id + "/"
    } else {
        type = 'POST'
        msg = 'New Position added Successfully'
        url = "/api/position/"
    }

    let form = $("#tagform");
    let data = getFormData(form[0]);
    let sk_length = $("input[name=skills]").val();
    let inteview_length = $("input[name=interview_det]").val();
    // if (sk_length == undefined){
    //     console.log("hello not value");
    // } else {
    //     console.log("hello value");
    // }
    if (form[0].checkValidity() == false || sk_length==undefined || inteview_length==undefined) {
        e.preventDefault();
        e.stopPropagation();
        $(".auto-suggest").addClass("tag-ctn-invalid");

    } else if ($("#job_description").val() == '') {
        $.confirm({
            title: 'Confirmation',
            content: 'Do you want to Upload without Job Description?',
            btnClass: 'btn-blue',
            buttons: {
                confirm: {
                    text: 'Proceed',
                    btnClass: 'btn-blue',
                    action: function() {
                        $(".close").click();
                        ajax_call({ url, type, msg, data });
                    }
                },
                cancel: function() {}
            }
        });
    } else {
        ajax_call({ url, type, msg, data });
        $(".auto-suggest").removeClass("tag-ctn-invalid");
    }
};

function candidatesubmitForm(e, rec_id) {
    let form = $("#candidateform");
    let form_data = new FormData($("#candidateform")[0]);
    // for (var value of form_data.values()) {
    //    console.log(value); 
    // }
    let sk_length = $("input[name=skills]").val();
    let np = $("input[name=notice_period]").val();
    let cctc = $("input[name=current_ctc]").val();
    let ectc = $("input[name=expected_ctc]").val();
    console.log(sk_length);
    // let inteview_length = $("input[name=interview_det]").val();
    $('input[name="emp_internal"]').click(function() {
        var inputValue = $(this).attr("value");
        if (inputValue != 0) {
            $("#notice_period").attr("required", true);
            $("#status").attr("required", true);
            $("#current_ctc").attr("required", true);
            $("#expected_ctc").attr("required", true);
        }
    });
    if (form[0].checkValidity() == false || sk_length == undefined || np == undefined|| cctc == undefined|| cctc == undefined) {
        e.preventDefault();
        e.stopPropagation();
        $(".auto-suggest").addClass("tag-ctn-invalid");
    } else {
        $(".auto-suggest").removeClass("tag-ctn-invalid");
        let type = "POST";
        let url = "/api/addnewcandidate/" + rec_id + "/";
        let msg = "New Candidate added Successfully";
        ajax_call({ type, url, msg, form_params: true, data: form_data });
    }
    // if (inteview_length != undefined) {
    //     $(".auto-suggest").removeClass("tag-ctn-invalid");
    // }
    form.addClass("was-validated");

    return false;
}

function addclientform(e){
    let form = $("#clientform");
    let form_data = new FormData($("#clientform")[0]);
    let cli_name_length = $("input[name=cli_name]").val();
    let pro_name_length = $("input[name=project_name]").val();
    let cli_loc_length  = $("input[name=cli_location]").val();
    let pro_id_length = $("input[name=project_manager]").val();

    if (form[0].checkValidity() == false || cli_name_length.length == 0 || pro_name_length.length == 0 || pro_id_length.length == 0) {
        e.preventDefault();
        e.stopPropagation();
        form.addClass("was-validated");
        return false;
    } else {
        $(".auto-suggest").removeClass("tag-ctn-invalid");
        let type = "POST";
        let url = "/api/addclient/";
        let msg = "New Client added Successfully";
        ajax_call({ type, url, msg, form_params: true, data: form_data });
    }
}



function deleteForm(e) {
    $.confirm({
        icon: "fa fa-trash-alt",
        title: "DELETE",
        content: "Are you Sure you want to delete this record",
        theme: "dark",
        type: "red",
        typeAnimated: true,
        buttons: {
            tryAgain: {
                text: "Ok",
                btnClass: "btn-red",
                action: function() {}
            },
            Close: function() {}
        }
    });
}

$(document).ready(function() {
    var date_input = $('input[id="date"]'); //our date input has the name "date"
    var container =
        $(".bootstrap-iso form").length > 0 ?
        $(".bootstrap-iso form").parent() :
        "body";
    var options = {
        format: "dd/mm/yyyy",
        container: container,
        todayHighlight: true,
        autoclose: true
    };
    date_input.datepicker(options);
    $(".bill_start_date").datepicker("setDate", new Date());
    // $('.on_board_date').datepicker("setDate", new Date());
    $("#add_new_position").on("click", function() {
        position_id = undefined;
        var client_code = $("#client_name").val();
        get_projects(client_code);
    });

    $("#client_name").on("change", function() {
        $("#project_name").empty();
        var client_code = $(this).val();
        get_projects(client_code);
    });

    function get_projects(client_code) {
        var data = ajax_call({ url: "/api/projects/" + client_code, type: "GET", call_back });

        function call_back(data) {
            if ($.isEmptyObject(data.data)) {
                $("#project_name").append("<option>No Project Details</option>");
            } else {
                $.each(data.data, function(code, data) {
                    var personalList = "<option value=" + data.code + ">" + data.name + "</option>";
                    $("#project_name").append(personalList);
                });
            }
        }
    }

    var skillData = [];
    var data = ajax_call({ url: "/api/skillset/", type: "GET", call_back: skill_set_det });

    function skill_set_det(data) {
        var sk_data = data.data;
        for (var i = 0; i < sk_data.length; i++) {
            skillData.push({ id: sk_data[i], name: sk_data[i] });
        }
    }
    var skills = $("#skills").tagSuggest({
        data: skillData,
        sortOrder: "name",
        maxDropHeight: 200,
        name: "skills"
    });

    var EmployeeData=[];
    var interviewData = [];
    var data = ajax_call({ url: "/api/employee/", type: "GET", call_back: emp_det });

    function emp_det(data) {
        var emp_data = data.data;
        for (var i = 0; i < emp_data.length; i++) {
            interviewData.push({
                id: emp_data[i]["id"],
                name: emp_data[i]["name"] + " " + "(" + emp_data[i]["email"] + ")"
                // email:
            });

            EmployeeData.push({
                id: emp_data[i]["id"],
                name: emp_data[i]["id"],
                employee:  emp_data[i]["name"]

            });

        }
    }

    var interview_det = $("#interview_det").tagSuggest({
        data: interviewData,
        sortOrder: "name",
        maxDropHeight: 200,
        name: "interview_det"
    });

    $("#emp_id").change(function () {
    let selectedEmpId = $("#emp_id" ).val();
    for(i=0; i<EmployeeData.length;i++){
    if(EmployeeData[i].id === selectedEmpId){
    $('#emp_name').val(EmployeeData[i].employee);
    break;
    }
    }
    });

    $("#emp_id").typeahead({
        source:EmployeeData
    });

    // dataTables
    $("#example").DataTable();
    $("#position_table").DataTable();

    $('input[name="billing_type"]').click(function() {
        let inputValue = $(this).attr("value");
        if (inputValue == 0) {
            $("#date").attr("disabled", true);
            $("#date").val("");
        } else {
            $("#date").attr("disabled", false);
            $(".bill_start_date").datepicker("setDate", new Date());
        }
    });
    $('input[name="client_interview"]').click(function() {
        let inputValue = $(this).attr("value");
        if (inputValue == 0) {
            $("#billing_type").val("0");
        } else {
            $("#billing_type").val("1");
            $("#date").attr("disabled", false);
            $(".bill_start_date").datepicker("setDate", new Date());
        }
    });
    $('input[name="emp_internal"]').click(function() {
        let inputValue = $(this).attr("value");
        if (inputValue == 0) {
            $("#emp_id").attr("disabled", true);
            $(".notice_details").show();
            $(".ctc_dtails").show();
        } else {
            $("#emp_id").attr("disabled", false);
            $(".notice_details").hide();
            $(".ctc_dtails").hide();
        }
    });
    $("#emp_id").attr("required", true);
    $(".notice_details").hide();
    $(".ctc_dtails").hide();
});

function info_box(rec_id) {
    $("#approvalModal").modal("show");
    let url = document.URL.split("/");
    ajax_call({
        url: "http://" + url[2] + "/api/approvals/" + rec_id,
        type: "GET",
        call_back: approval_data
    });

}
function approval_data(res) {
    $("#no_of_positions").val(res["data"][0]["no_of_positions"]);
    $("#experience").val(res["data"][0]["experience"]);
    $("#qualification").val(res["data"][0]["qualification"]);
    $("#designation").val(res["data"][0]["designation"]);
    $("#demand_type").val(res["data"][0]["demand_type"]);
    if (res["data"][0]["client_interview"] == true) {
        $("#client_interview_yes").prop("checked", true);
        $(".client_bill_details").show();
    } else {
        $("#client_interview_no").prop("checked", true);
        $(".client_bill_details").hide();
    }
    if (res["data"][0]["billable"] == true) {
        $("#billing_type_yes").prop("checked", true);
    } else {
        $("#billing_type_no").prop("checked", true);
    }
    $("#job_type").val(res["data"][0]["job_type"]);
    $("#location").val(res["data"][0]["location"]);
    $("#date").val(res["data"][0]["bill_date"]);
    $("#job_description").val(res["data"][0]["job_description"]);
    $('#interview_details').val(res['data'][0]['interview_details']);
}

function editPositionForm(rec_id) {
    position_id = rec_id;
    $('#myModal').modal('show');
    $("#reset,.close").click(function() {
        location.reload();
    });
    $(".modal-title-header").text($(".modal-title-header").text().replace("Add New", "Edit"));
    var url = document.URL.split("/");
    var data = ajax_call({ url: "http://" + url[2] + "/api/approvals/" + rec_id, type: "GET", call_back: update_data });
}


function update_data(res) {
    $("#no_of_positions").val(res["data"][0]["no_of_positions"]);
    $("#client_name").val(res['data'][0]['client_name']);
    $('#project_name').find('option').remove().end().append("<option value=" + res['data'][0]['project_code'] + ">" + res['data'][0]['project_name'] + "</option>");
    $("#experience").val(res['data'][0]['experience']);
    // $("#ex6SliderVal").text(res['data'][0]['no_of_positions']);
    $("#qualification").val(res['data'][0]['qualification']);
    $("#designation").val(res['data'][0]['designation']);
    $("#demand_type").val(res['data'][0]['demand_type']);
    if (res['data'][0]['client_interview'] == true) {
        $("#client_interview_yes").prop("checked", true);
    } else {
        $("#client_interview_no").prop("checked", true);
    }
    $("#location").val(res["data"][0]["location"]);
    $("#request_type").val(res['data'][0]['request_type']);
    $('#skills').tagSuggest().clear();
    $('#skills').tagSuggest().setValue(res['data'][0]['skills']);
    $('#interview_det').tagSuggest().clear();
    $('#interview_det').tagSuggest().setValue(res['data'][0]['interview_det']);
    $("#job_type").val(res['data'][0]['job_type']);
    if (res['data'][0]['billable'] == true) {
        $("#billing_type_yes").prop("checked", true);
    } else {
        $("#billing_type_no").prop("checked", true);
        $("#date").attr("disabled", true);
    }
    $("#job_description").val(res['data'][0]['job_description']);
    }

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            //Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie("csrftoken");

function approved_form(rec_id, name, status, msg) {
    var data = {
        name: name,
        status: status
    };
    $.ajax({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        type: "PUT",
        url: "/api/approvals/" + rec_id + "/",
        data: data,
        success: function(data) {
            success_util(rec_id + " " + msg);
        }
    });
}

function approvalForm(rec_id) {
    $.confirm({
        animation: "zoom",
        closeAnimation: "scale",
        title: "Are you sure want to approve?",
        content: "" +
            '<form action="" class="formName">' +
            '<div class="form-group">' +
            "<label>Feedback Review</label>" +
            '<textarea rows="4" placeholder="Feedback" class="name form-control" maxlength="250"></textarea>' +
            "</div>" +
            "</form>",
        closeIcon: true,
        buttons: {
            reject: function() {
                var name = this.$content.find(".name").val();
                var status = 0;
                if (!name) {
                    $.alert("Please enter valuable feedback");
                    return false;
                }
                var msg = "Rejected Successfully";
                approved_form(rec_id, name, status, msg);
            },
            formSubmit: {
                text: "Accept",
                btnClass: "btn-green",
                action: function() {
                    var name = this.$content.find(".name").val();
                    var status = 1;
                    var msg = "Approved Successfully"
                    approved_form(rec_id, name, status, msg);
                }
            }
        },

        onContentReady: function() {
            // bind to events
            var jc = this;
            this.$content.find("form").on("submit", function(e) {
                // if the user submits the form by pressing enter in the field.
                e.preventDefault();
                jc.$$formSubmit.trigger("click"); // reference the button and click it
            });
        }
    });
}

function approvalcandidateForm(rec_id, can_id) {
    $("#candidate_ratings").data("rec_id", rec_id);
    $("#candidate_ratings").data("can_id", can_id);
}

function rmg_remarks_candidate(e) {
    let can_id = $("#candidate_ratings").data("can_id");
    let rec_id = $("#candidate_ratings").data("rec_id");
    let data = {
      rec_id: rec_id,
      can_id: can_id,
      rmg_remarks : $("#rmg_comments").val(),
      status : $("#rmg_status").val()
    };
    ajax_call({
        type: "PUT",
        url: "/api/addnewcandidate/" + rec_id + "/",
        msg: "Candidate Selected for "+ rec_id,
        data: JSON.stringify(data)
    });
}

function candidate_feedback(e) {
    let form = $("#interviewform");
    let sk_length = $("input[name=skills]").val();
    if (form[0].checkValidity() == false|| sk_length==undefined) {
        e.preventDefault();
        e.stopPropagation();
        form.addClass("was-validated");
        return false;
    }
    let form_data = new FormData($("#interviewform")[0]);
    form_data.append('rec_id', $("#candidate_ratings").data("rec_id"));
    form_data.append('can_id', $("#candidate_ratings").data("can_id"));
    ajax_call({
        type: "POST",
        url: "/api/feedback/",
        msg: "Feedback added Successfully",
        form_params: true,
        data: form_data
    });
}

function interviewer_feedback(rec_id, c_id) {
    $("#interview_det").data("recID", rec_id);
    $("#interview_det").data("cusID", c_id);

    let table = $("#candidate_interview tbody");

    let construct_table = data => {
        table.empty();
        $.each(data.data.feedbacks, function(a, b) {
            var row = "<tr>";
            row +=
                "<td>" +
                b.emp_id +
                " - " +
                b.emp_name +
                "</td><td>" +
                b.ratings +
                "</td><td>" +
                b.skill_set +
                "</td><td wrap>" +
                b.remarks +
                "</td><td>"+
                b.ts +
                "</td>";
            if (b.approved == true) {
                row += "<td>Selected</td>";
            } else {
                row += "<td>Rejected</td>";
            }
            if (b.file != "None") {
                row += "<td>\
                <a href='/static/doc/" + b.file + "' target='_blank'>\
                <span class='icon-bodate_timex-2x'>\
                  <i class='fa fa-file-word-o'></i>\
                </span>\
              </a></td>";
            } else {
                row += "<td></td>";
            }
            row += "</tr>";
            table.append(row);
        });
        $("#candidate_interview").DataTable();
    }

    ajax_call({
        type: "GET",
        url: "/api/feedback/" + c_id + "/",
        call_back: construct_table
    });
}

function interviewer_details(rec_id, c_id) {
  $("#interview_det").data("recID", rec_id);
  $("#interview_det").data("cusID", c_id);

  let construct_interviewer_details = data =>{
    $('#interview_det').tagSuggest().clear();
    $('#interview_det').tagSuggest().setValue(data.data.interviewer_details);
  }
  ajax_call({
    type: "GET",
    url: "/api/feedback/" + c_id + "/",
    call_back: construct_interviewer_details

  });
}

function add_interview_details(e) {
    let rec_id = $("#interview_det").data("recID");
    let cus_id = $("#interview_det").data("cusID");
    let date_time = $("#date_time").val();
    let interview_det = JSON.parse($("input[name='interview_det']").val());

    if (interview_det.length == 0 || date_time.length == 0) {
        e.preventDefault();
        e.stopPropagation();
        alert("Please enter  date and time of interview");
        return false;
    }

    let data = {
        interview_det: interview_det,
        can_id: cus_id,
        date_time: date_time
    };
    ajax_call({
        type: "PUT",
        url: "/api/addnewcandidate/" + rec_id + "/",
        msg: "Interviewer details updated Successfully",
        data: JSON.stringify(data)
    });
}

function candidate_approval(can_id, rec_id) {
    $("#candidate_comments").data("canID", can_id);
    $("#candidate_comments").data("recID", rec_id);
}

function add_candidate_remarks(e, no_of_positions, selected_candidate_count) {

    let can_id = $("#candidate_comments").data("canID");
    let rec_id = $("#candidate_comments").data("recID");
    let form = $("#candidate_status_form");
    let form_data = new FormData($("#candidate_status_form")[0]);
    if (form[0].checkValidity() == false) {
        e.preventDefault();
        e.stopPropagation();
        form.addClass("was-validated");
        return false;
    }

    // checking selected no of candidates
    if (parseInt(no_of_positions) <= parseInt(selected_candidate_count) && parseInt($('#candidate_status').val())) {
        $.confirm({
            icon: "fas fa-exclamation-triangle",
            title: rec_id + ' ' + 'Position closed',
            content: 'Do you want to continue?',
            btnClass: 'btn-blue',
            closeIcon: true,
            buttons: {
                confirm: {
                    text: 'Proceed',
                    btnClass: 'btn-blue',
                    action: function() {
                        hr_approved_candidate (can_id, form_data);
                    }
                },
                cancel: function() {}
            }
        });
    } else {
        hr_approved_candidate (can_id, form_data);
    }
}

function hr_approved_candidate (can_id, form_data) {
    $.ajax({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        type: "PUT",
        url: "/api/candidate/" + can_id + "/",
        processData: false,
        contentType: false,
        data: form_data,
        success: function(data, status) {
          let msg = JSON.parse(data).msg;
            if (status == "success") {
                success_util(msg);
            }
        }
    });
}

function feedbackForm(title, remarks) {
    $.confirm({
        animationBounce: 1.5,
        title: title,
        content: remarks,
        type: "blue",
        typeAnimated: true,
        closeIcon: true,
        buttons: {
            info: {
                btnClass: 'btn',
                text: 'Close'
            }
        }
    });
};


function editcandidateForm(rec_id,can_id,notice_period,current_ctc,expected_ctc) {
    $("#notice_period").data("canID", can_id);
    $("#notice_period").data("recID", rec_id);
    $("#notice_period").val(notice_period);
    $("#current_ctc").val(current_ctc);
    $("#expected_ctc").val(expected_ctc);

}

function editcandidateDetails(e) {
  let rec_id = $("#notice_period").data("recID");
  let can_id = $("#notice_period").data("canID");
  let data = {
      rec_id: rec_id,
      can_id: can_id,
      notice_period:$("#notice_period").val(),
      current_ctc:$("#current_ctc").val(),
      expected_ctc:$("#expected_ctc").val(),
      role:"RMG"
  };
  ajax_call({
      type: "PUT",
      url: "/api/addnewcandidate/" + rec_id + "/",
      msg: "Candidate CTC Updated Successfully",
      data: JSON.stringify(data)
  });
}

// function approved_candidate_list(rec_id){
//     $(".main ol").append('<li class="breadcrumb-item position">\
//             <a href="#">Selected Candidates</a></li>');
// }