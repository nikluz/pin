// Generated by CoffeeScript 1.4.0
(function() {
  var add_pin_to_user, pin_count, remove_pin_from_user;

  pin_count = 0;

  $(".select_pins").click(function() {
    var pin_id;
    pin_id = $(this).attr('pinid');
    console.log(pin_id);
    if ($(this).hasClass("selected")) {
      return remove_pin_from_user(pin_id, $(this));
    } else {
      return add_pin_to_user(pin_id, $(this));
    }
  });

  add_pin_to_user = function(pin_id, button) {
    return $.ajax("/register/api/users/me/coolpins/" + pin_id + "/", {
      type: 'PUT',
      dataType: 'json',
      success: function(data) {
        button.addClass('selected');
        pin_count += 1;
        if (pin_count > 4) {
          return $('#continue_button').removeAttr('disabled');
        }
      }
    });
  };

  remove_pin_from_user = function(pin_id, button) {
    return $.ajax("/register/api/users/me/coolpins/" + pin_id + "/", {
      type: 'DELETE',
      dataType: 'json',
      success: function(data) {
        button.removeClass('selected');
        pin_count -= 1;
        if (pin_count < 5) {
          return $('#continue_button').attr('disabled', 'disabled');
        }
      }
    });
  };

  $("#continue_button").click(function() {
    return window.location.href = '3';
  });

}).call(this);
