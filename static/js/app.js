document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      // TODO: get data from inputs and show them in summary

    }



    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
    submit(e) {
      e.preventDefault();
      this.currentStep++;
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
      let user = '{{  }}'

      let all_checkbox_input_id = document.querySelectorAll('input[class="multiple_checkbox_input"]:checked');

      let checkbox_list_values = [];

      for(let x = 0, l = all_checkbox_input_id.length; x < l;  x++)
      {
          checkbox_list_values.push(all_checkbox_input_id[x].value);
      }

      let checkbox_string_values = checkbox_list_values.join(', ');
      // let final_checkbox_list = Array.of(checkbox_list_values);
      console.log(checkbox_string_values);
      this.updateForm();
              let bags = $("input[name='bags']").val();
              // let organization = $("input[name='organization']").val();
              let organization = $("input[name='organization']:checked").val();
              let address = $("input[name='address']").val();
              let city = $("input[name='city']").val();
              let postcode = $("input[name='postcode']").val();
              let date = $("input[name='date']").val();
              let time = $("input[name='time']").val();
              let more_info = $("textarea#pick_up_comment").val();
              // let categories = $("input[name='categories']:checked")
              //   .map(() => { return this.value }).get()
              let categories = checkbox_string_values
              let phone = $("input[name='phone']").val();
              // let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

              $.ajax({
                url: '/charity_donation/add_donation/',
                type: 'post',
                data: {
                    'categories': categories,
                    'quantity': bags,
                    'institution': organization,
                    'address': address,
                    'city': city,
                    'zip_code': postcode,
                    'pick_up_date': date,
                    'pick_up_time': time,
                    'pick_up_comment': more_info,
                    'csrfmiddlewaretoken': csrftoken,
                    'phone_number': phone,
                    'credentials': 'include',
                },
                success: function (data) {
                    alert("Dziękujemy, twoja darowizna została zarejestrowana!");
                    window.location.replace('/charity_donation/form_confirmation');
                },
                error : function(xhr,errmsg,err) {
                    alert(xhr.status + ": " + xhr.responseText);
    }
              });
    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }



  let second_button = document.getElementById("second_button");
  let third_button = document.getElementById("third_button");
  let fourth_button = document.getElementById("fourth_button");

  second_button.addEventListener('click', function () {
    let bags = $("input[name='bags']").val();
    let given_bags = document.querySelector('#bags');
    given_bags.textContent = given_bags.textContent + bags;
  })
  third_button.addEventListener('click', function () {
    let organization_pk = $("input[name='organization']:checked").val()
    // let organization = $("input[name='organization']:checked").nextSibling.nextSibling.firstChild
    // let organization = document.getElementById('organization_name')
    let inst_csrftoken = $("input[name='csrfmiddlewaretoken']").val();
              $.ajax({
                url: '/charity_donation/add_donation/',
                type: 'post',
                data: {
                    'organization_pk': organization_pk,
                    'csrfmiddlewaretoken': inst_csrftoken,
                },
                success: function (org_response) {
                    alert("Zaznaczono organizację");
                    let organization = org_response['organization']
                    let given_organization = document.querySelector('#organization');
                    given_organization.textContent = given_organization.textContent + organization
                },
                error : function(xhr,errmsg,err) {
                    alert(xhr.status + ": " + xhr.responseText);
                },
              });
    // let given_organization = document.querySelector('#organization');
    // given_organization.textContent = given_organization.textContent + organization
  })
  fourth_button.addEventListener('click', function () {
    let address = $("input[name='address']").val();
    let city = $("input[name='city']").val();
    let postcode = $("input[name='postcode']").val();
    let date = $("input[name='date']").val();
    let time = $("input[name='time']").val();
    let phone = $("input[name='phone']").val();
    let more_info = $("input[name='pick_up_comment']").val();

    let given_address = document.querySelector('#address');
    let given_city = document.querySelector('#city');
    let given_postcode = document.querySelector('#postcode');
    let given_phone = document.querySelector('#phone');
    let given_date = document.querySelector('#date');
    let given_time = document.querySelector('#time');
    let given_more_info = document.querySelector('#pick_up_comment');

    given_address.textContent = address;
    given_city.textContent = city;
    given_postcode.textContent = postcode;
    given_phone.textContent = phone;
    given_date.textContent = date;
    given_time.textContent = time;
    given_more_info.textContent = more_info;
  })
});
