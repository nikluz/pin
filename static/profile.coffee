removeRePin = (e, y) ->
  result = undefined
  result = window.confirm("Are you sure you want to remove this picture ?")
  if result
    $.get "/remove-from-own-getlist",
      pinid: e
      repinid: y
    , (response) ->
      id = undefined
      if response.error
        alert "An error occured, please refresh the page and try again later"
      else
        id = "#horz-pin" + e
        $(id).slideToggle()
      return

(->
  dragging_header_background = undefined
  otherX = undefined
  otherY = undefined
  rePin = undefined
  removeRePin = undefined
  x = undefined
  y = undefined
  rePin = (e) ->
    desc = undefined
    id = undefined
    desc = $(e).attr("data-description")
    id = $(e).attr("data-id")
    $("#repin-image").attr "src", "/static/tmp/pinthumb" + id + ".png"
    $("#description").html desc
    $("#repin-form").attr "action", "/add-to-your-own-getlist/" + id
    $(".category-list").val $(e).attr("data-category")
    return

  $("#save_thumbnail_edit").click ->
    location.reload true
    return

  $("#set_as_profile_pic").click ->
    picid = undefined
    picid = $(".modal .active img").attr("picid")
    $.get "/setprofilepic/" + picid, (response) ->
      location.reload true
      return


  dragging_header_background = false
  x = 0
  y = 0
  otherX = 0
  otherY = 0
  $("#header_background").mousedown (e) ->
    _ref = undefined
    _ref = undefined
    x = e.pageX
    y = e.pageY
    _ref = $(this).css("background-position").split(" ")
    otherX = _ref[0]
    otherY = _ref[1]
    dragging_header_background = true

  $("body").mouseup ->
    tempX = undefined
    tempY = undefined
    _ref = undefined
    tempX = undefined
    tempY = undefined
    _ref = undefined
    if dragging_header_background
      dragging_header_background = false
      _ref = $("#header_background").css("background-position").split(" ")
      otherX = _ref[0]
      otherY = _ref[1]
      tempX = parseInt(otherX.slice(0, +(otherX.length - 2) + 1 or 9e9))
      tempY = parseInt(otherY.slice(0, +(otherY.length - 2) + 1 or 9e9))
      $.post "/changebgpos",
        x: tempX
        y: tempY


  $("#header_background").mousemove (e) ->
    tempY = undefined
    upload = undefined
    tempY = undefined
    if dragging_header_background
      upload = false
      tempY = parseInt(otherY.slice(0, +(otherY.length - 2) + 1 or 9e9))
      $(this).css "background-position", otherX + " " + (tempY + (e.pageY - y)) + "px"  if tempY + (e.pageY - y) < 0

  $("#switch5_wrapper").mouseover ->
    $("#menu5").show()

  $("#switch5_wrapper").mouseout ->
    $("#menu5").hide()

  $("#myTab a").click (e) ->
    e.preventDefault()
    $(this).tab "show"
    return

  return