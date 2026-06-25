(function () {
	function hidePreloader() {
		$(".preloader").fadeOut(500, function () {
			$(".wrapper").fadeIn(500);
		});
	}
	if (document.readyState === "complete") {
		hidePreloader();
	} else {
		$(window).on("load", hidePreloader);
	}
})();

$(document).ready(function () {

	$(function () {
		function closeMenu() {
			const body = $("body");
			body.removeClass("mobile tablet desktop close-menu open-menu expand-menu");

			$(".side-bar-close").off("click");
			$(".side-bar-body").off("mouseenter mouseleave");

			if (window.matchMedia("(max-width: 767px)").matches) {
				body.addClass("mobile close-menu");

				$(".side-bar-close").on("click", function () {
					body.toggleClass("close-menu open-menu");
				});
			} else if (window.matchMedia("(min-width: 768px) and (max-width: 1199px)").matches) {
				body.addClass("tablet");

				$(".side-bar-close").on("click", function () {
					if (!body.hasClass("open-menu") && !body.hasClass("close-menu")) {
						body.addClass("open-menu");
						return;
					}
					if (body.hasClass("close-menu")) {
						body.removeClass("close-menu").addClass("open-menu");
					} else {
						body.removeClass("open-menu").addClass("close-menu");
					}
				});
			} else {
				body.addClass("desktop");

				$(".side-bar-close").on("click", function () {
					if (!body.hasClass("open-menu") && !body.hasClass("close-menu")) {
						body.addClass("close-menu");
						return;
					}
					if (body.hasClass("close-menu")) {
						body.removeClass("close-menu").addClass("open-menu");
					} else {
						body.removeClass("open-menu").addClass("close-menu");
					}
				});

				$(".side-bar-body").on("mouseenter", function () {
					if (body.hasClass("close-menu")) {
						body.addClass("expand-menu");
					}
				}).on("mouseleave", function () {
					body.removeClass("expand-menu");
				});
			}
		}
		closeMenu();

		// Run on resize
		$(window).resize(function () {
			closeMenu();
		});

		$(".form-control-password").each(function () {
			const $this = $(this);
			$this.append('<span class="eye-icon"></span>');

			const $icon = $this.find('.eye-icon');
			const $input = $this.find('input')


			$icon.on("click", function () {
				const type = $input.attr('type') === 'password' ? 'text' : 'password';
				$this.toggleClass("show");
				$input.attr('type', type);
			});
		});

		$('.side-bar .dropdown-toggle').on('click', function (e) {
			e.preventDefault();

			const $menu = $(this).next('.dropdown-menu');
			const $parent = $(this).closest('.dropdown');
			$('.side-bar .dropdown-menu').not($menu).slideUp(300).removeClass('show');
			$('.side-bar .nav-item.dropdown').not($parent).removeClass('open');
			if ($menu.hasClass('show')) {
				$menu
					.slideUp(300)
					.removeClass('show');
			} else {
				$menu
					.stop(true, true)
					.slideDown(300)
					.addClass('show');
			}
			$parent.toggleClass('open');
		});


		$('.dropdown-menu li.active').each(function () {
			$(this).closest('.dropdown .dropdown-menu').css('display', 'block');
		});


	});



	$(window).scroll(function () {
		var height = $(window).scrollTop();

		if (height > 300) {
			$('header').addClass('sticky');
		} else {
			$('header').removeClass('sticky');
		}
	});

	function otp() {
		$('.otp').find('input').each(function () {
			$(this).attr('maxlength', 1);
			$(this).on('keyup', function (e) {
				var parent = $($(this).parent());

				if (e.keyCode === 8 || e.keyCode === 37) {
					var prev = parent.find('input#' + $(this).data('previous'));

					if (prev.length) {
						$(prev).select();
					}
				} else if ((e.keyCode >= 48 && e.keyCode <= 57) || (e.keyCode >= 65 && e.keyCode <= 90) || (e.keyCode >= 96 && e.keyCode <= 105) || e.keyCode === 39) {
					var next = parent.find('input#' + $(this).data('next'));

					if (next.length) {
						$(next).select();
					} else {
						if (parent.data('autosubmit')) {
							parent.submit();
						}
					}
				}
			});
		});
	}
	otp();

	function setupDropdowns() {
		$("table .dropdown").each(function () {
			var dropDown = $(this);
			var dropDownLink = dropDown.find("> *");

			dropDown.off("mouseenter mouseleave");
			dropDownLink.off("click");
			$(document).off("click.dropdown");

			dropDownLink.on("click", function (e) {
				//e.preventDefault();
				//e.stopPropagation();

				// Close other dropdowns
				$("table .dropdown").not(dropDown).removeClass("show dropdown-up dropdown-down");

				// Toggle this dropdown
				dropDown.toggleClass("show");

				// Remove any previous direction classes
				dropDown.removeClass("dropdown-up dropdown-down");

				// Only proceed if showing
				if (!dropDown.hasClass("show")) return;

				const $menu = dropDown.find(".dropdown-menu");
				const menuHeight = $menu.outerHeight();

				const table = dropDown.closest("table");
				const tableOffsetTop = table.offset().top;
				const tableHeight = table.outerHeight();
				const tableBottom = tableOffsetTop + tableHeight;

				const iconOffset = dropDown.offset().top;
				const spaceBelowInTable = tableBottom - (iconOffset + dropDown.outerHeight());
				const spaceAboveInTable = iconOffset - tableOffsetTop;

				if (spaceBelowInTable < menuHeight && spaceAboveInTable > menuHeight) {
					dropDown.addClass("dropdown-up");
				} else {
					dropDown.addClass("dropdown-down");
				}
			});

			$(document).on("click.dropdown", function (e) {
				if (!$(e.target).closest("table .dropdown").length) {
					$("table .dropdown").removeClass("show dropdown-up dropdown-down");
				}
			});
		});

	}

	$(document).ready(function () {
		setupDropdowns();
	});

	let resizeTimer;
	$(window).on("resize", function () {
		clearTimeout(resizeTimer);
		resizeTimer = setTimeout(setupDropdowns, 250);
	});

	$(function () {
		$('.upload-block').each(function () {
			const block = $(this);
			const area = block.find('.upload-area');
			const infoArea = block.find('.upload-info');
			const input = block.find('.file-input');
			const name = block.find('.file-name');
			const img = block.find('.preview');
			const clear = block.find('.clear');
			const imageInfo = block.find('.image-info');

			area.on('click', () => input.click());

			input.on('change', function () {
				const file = this.files[0];
				if (file && file.type.startsWith('image/')) {
					infoArea.addClass('show');
					const reader = new FileReader();

					reader.onload = e => {
						img.attr('src', e.target.result).show();
						name.text(file.name);
						clear.show(); // Show the Clear button when a file is selected

						// Create an Image object to get width and height
						const image = new Image();
						image.onload = function () {
							const width = image.width;
							const height = image.height;

							// FILE SIZE IN KB (2 decimal places)
							const sizeKB = (file.size / 1024).toFixed(2);
							//imageInfo.text(`${width}x${height}px • ${sizeKB} KB`);
							//imageInfo.text(`${sizeKB} Kb`);
						};
						image.src = e.target.result;
					};

					reader.readAsDataURL(file);

				} else {
					infoArea.removeClass('show');
					name.text('');
					img.hide().attr('src', '#');
					imageInfo.text('');
					clear.hide(); // Hide the Clear button if the file is not valid
				}

			});

			area.on('dragover', e => {
				e.preventDefault();
				area.addClass('dragover');
			});

			area.on('dragleave', () => area.removeClass('dragover'));

			area.on('drop', function (e) {
				e.preventDefault();
				area.removeClass('dragover');
				const file = e.originalEvent.dataTransfer.files[0];
				input[0].files = e.originalEvent.dataTransfer.files;
				input.trigger('change');
			});

			clear.on('click', () => {
				infoArea.removeClass('show');
				input.val('');
				name.text('');
				img.hide().attr('src', '#');
				imageInfo.text('');
				clear.hide(); // Hide the Clear button after clearing the file
			});
		});
	});

	$('.form-dob').each(function () {
		$dayValue = $(this).find('.dob-day');
		$monthValue = $(this).find('.dob-month');
		$yearValue = $(this).find('.dob-year');

		const monthNames = [
			//"Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
			"January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
		];

		$yearValue.append(`<option value="0" selected hidden>YYYY</option>`);
		$monthValue.append(`<option value="0" selected hidden>MM</option>`);
		$dayValue.append(`<option value="0" selected hidden>DD</option>`);

		const currentYear = new Date().getFullYear();
		const maxYear = currentYear;
		for (let y = maxYear; y >= 1900; y--) {
			$($yearValue).append(`<option value="${y}">${y}</option>`);
		}

		$.each(monthNames, function (index, month) {
			$($monthValue).append(`<option value="${index + 1}">${month}</option>`);
		});

		for (let d = 1; d <= 31; d++) {
			$($dayValue).append(`<option value="${d}">${d}</option>`);
		}

		// Function to update day dropdown
		function updateDays() {
			const year = parseInt($($yearValue).val());
			const month = parseInt($($monthValue).val());

			if (!year || !month) return;

			const daysInMonth = new Date(year, month, 0).getDate();

			$($dayValue).empty();
			for (let d = 1; d <= daysInMonth; d++) {
				$($dayValue).append(`<option value="${d}">${d}</option>`);
			}
		}

		// Populate default days (in case all 3 are already pre-selected)
		//updateDays();

		// Event listeners to update days
		$($monthValue, $yearValue).change(function () {
			//updateDays();
		});

	});

	$(function () {

		$('input.form-calendar.dob').daterangepicker({
			singleDatePicker: true,
			showDropdowns: true,
			autoUpdateInput: false,
			minYear: 1901,
			drops: 'auto',
			container: 'body',
			maxYear: parseInt(moment().format('YYYY'), 10),
			locale: {
				format: 'DD MMM, YYYY'
			}
		});
		$('input.form-calendar.dob').on('apply.daterangepicker', function (ev, picker) {
			$(this).val(picker.startDate.format('DD MMM, YYYY'));
		});

		$('input.form-calendar.time').daterangepicker({
			timePicker: true,
			singleDatePicker: true,
			autoUpdateInput: false,
			showDropdowns: true,
			drops: 'auto',
			container: 'body',
			locale: {
				format: 'DD MMM, YYYY, hh:mm A'
			}
		});
		$('input.form-calendar.time').on('apply.daterangepicker', function (ev, picker) {
			$(this).val(picker.startDate.format('DD MMM, YYYY, hh:mm A'));
		});

		$('input.form-calendar').on('show.daterangepicker', function () {
			$('.modal').addClass('calendar-active');
		});

		$('input.form-calendar').on('hide.daterangepicker', function () {
			$('.modal').removeClass('calendar-active');
		});

	});

	$(function () {


		$('.date-filter').each(function () {
			var start = moment().subtract(29, 'days');
			var end = moment();
			var button = $(this).find('button');
			var value = $(this).find('input');
			var dateData = $(this).find('#dateFilter');

			$(button).daterangepicker({
				startDate: start,
				endDate: end,
				opens: 'left',
				cancelClass: 'btn-light',
				ranges: {
					'Today': [moment(), moment()],
					'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
					'Last 7 Days': [moment().subtract(6, 'days'), moment()],
					'Last 30 Days': [moment().subtract(29, 'days'), moment()],
					'This Month': [moment().startOf('month'), moment().endOf('month')],
					'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
				}
			}, function (start, end) {
				$(value).val(start.format('DD/MM/YYYY') + ' - ' + end.format('DD/MM/YYYY'));
				$(dateData).text(start.format('D MMM') + ' - ' + end.format('D MMM'));
			});
		});
	});

	$(".multi-select-dropdown").each(function () {
		var dropdown = $(this);
		var multiDisplay = dropdown.find('.multi-select');
		var multiList = dropdown.find('.multi-select-list');
		var multiSelectInput = dropdown.find('.multi-select-input');
		var multiListFilter = dropdown.find('.multi-select-filter input');
		var multiListFilterWrapper = dropdown.find('.multi-select-filter');
		var multiListItem = dropdown.find('.multi-select-item');

		multiListFilterWrapper.after(`<div class="multi-select-not-found" style="display:none;">Not found</div>`);


		multiList.find('.multi-select-item.selected').each(function () {
			var id = $(this).data('id');
			var value = $(this).data('value');

			// Avoid duplicates
			if (multiDisplay.find('.selected-item[data-id="' + id + '"]').length === 0) {
				var selectedItem = $('<span class="selected-item" data-id="' + id + '" data-value="' + value + '">' + value + '<span class="remove-btn">&times;</span></span>');
				selectedItem.insertBefore(multiSelectInput);
			}
		});

		updateInputField();

		multiDisplay.on('click', function (e) {
			e.stopPropagation();
			$('.multi-select-list').not(multiList).removeClass('show');
			multiList.toggleClass('show');
		});

		multiList.on('click', '.multi-select-item', function (e) {
			e.stopPropagation();
			var id = $(this).data('id');
			var value = $(this).data('value');

			if (multiDisplay.find('.selected-item[data-id="' + id + '"]').length === 0) {
				var selectedItem = $('<span class="selected-item" data-id="' + id + '" data-value="' + value + '">' + value + '<span class="remove-btn">&times;</span></span>');
				selectedItem.insertBefore(multiSelectInput);
				$(this).addClass('select');
				updateInputField();
			}
		});

		multiDisplay.on('click', '.remove-btn', function (e) {
			e.stopPropagation();
			var id = $(this).closest('.selected-item').data('id');

			$(this).closest('.selected-item').remove();

			$('.multi-select-item[data-id="' + id + '"]').removeClass('select');
			updateInputField();

		});

		multiListFilter.on('keyup', function () {
			var value = $(this).val().toLowerCase();
			var searchR = $(this).closest('.multi-select-list');

			var visibleCount = 0;

			searchR.find('.multi-select-item').each(function () {
				var isMatch = $(this).text().toLowerCase().indexOf(value) > -1;
				$(this).toggle(isMatch);
				if (isMatch) visibleCount++;
			});

			if (visibleCount === 0) {
				multiList.find('.multi-select-not-found').show();
			} else {
				multiList.find('.multi-select-not-found').hide();
			}
		});


		function updateInputField() {
			let values = [];
			multiDisplay.find('.selected-item').each(function () {
				var id = $(this).data('id');
				var value = $(this).data('value');
				values.push(id + ':' + value);
			});
			multiSelectInput.val(values.join(", "));
			if (values.length == 0) {
				multiDisplay.find('.select-placeholder').show();
			} else {
				multiDisplay.find('.select-placeholder').hide();
			}
		}

	});

	$(window).on('click', function (e) {
		if (!$(e.target).closest('.multi-select-dropdown').length) {
			$('.multi-select-list').removeClass('show');
			$('.multi-select-item').show();
			$('.multi-select-filter input').val('');
			$('.multi-select-not-found').hide();
		}
	});

	function tableResponsive() {
		$('.table').each(function () {
			const $table = $(this);

			if (window.matchMedia("(max-width: 767px)").matches) {
				if ($table.hasClass('responsive-applied')) return;
				$table.addClass('responsive-applied');
				$('tbody tr:not(.expand-header)').hide();

				const theadLength = $table.find('thead tr td, thead tr th').length;
				const bodyTitle = [];
				$table.find('thead tr td, thead tr th').each(function () {
					bodyTitle.push($(this).clone().children().remove().end().text().trim());
				});

				const firstTwoSpans = $('tr td').slice(0, 2).map(function () {
					return $('<span>', {
						class: $(this).attr('class'),
						html: $(this).html()
					});
				}).get();

				const $expandContent = $('<div></div>').append(firstTwoSpans);

				const $spanWrapper = $(`
					<tr class="thead-tr">
						<td colspan="${theadLength}"></td>
					</tr>
				`);

				$spanWrapper.find('td').append($expandContent);
				$table.find('thead').append($spanWrapper);



				$table.find('tbody tr').each(function () {
					const $tr = $(this);

					const textHtml = $tr.find('td, th').slice(0, 2).map(function () {
						return `<span>${$(this).html().trim()}</span>`;
					}).get().join('');

					const $newTr = $(`
						<tr class="expand-header">
							<td colspan="${theadLength}">
								<div class="expand-content">
									${textHtml}
									<span class="expand-btn"></span>
								</div>
							</td>
						</tr>
					`);

					$tr.after($newTr);

					$tr.find('> *').each(function (index) {
						$(this).attr('data-label', bodyTitle[index]);
					});
				});

			} else {
				$table.find('.thead-tr').remove();
				$('tbody tr:not(.expand-header)').removeAttr('style');
				$table.removeClass('responsive-applied');
				$table.find('.expand-header').remove();
				$table.find('[data-label]').removeAttr('data-label');
			}
		});
	}
	tableResponsive();

	$(window).resize(function () {
		tableResponsive();
	});

	$(document).on('click', 'table .expand-header .expand-btn', function () {
		const $expandHeader = $(this).closest('.expand-header');
		const $expandTr = $expandHeader.prev('tr');

		if ($expandTr.is(':visible')) {
			$expandTr.slideUp(200);
			$expandHeader.removeClass('open');
		} else {
			$expandHeader.closest('tbody').find('tr:not(.expand-header)').slideUp(200);
			$expandHeader.closest('tbody').find('.expand-header').not($expandHeader).removeClass('open');

			$expandTr.slideDown(300);
			$expandHeader.addClass('open');
		}
	});

	function customSelect() {
		function create_custom_dropdowns() {
			$('.form-select').each(function () {
				var $select = $(this);
				var selectedOption = $select.find('option:selected');
				var placeholder = selectedOption.text() || 'Select';

				if (!$select.next().hasClass('custom-select')) {
					var dropdownHtml = `
					<div class="custom-select ${$select.attr('class') || ''}" tabindex="0">
						<span class="current"><span class="custom-placeholder">${placeholder}</span></span>
						<div class="list">
							<div class="custom-select-search">
								<input class="form-control" type="text" placeholder="Search..." />
							</div>
							<ul></ul>
							<div class="custom-select-not-found" style="display:none;">Not found</div>
						</div>
					</div>`;
					$select.after(dropdownHtml);

					var $dropdown = $select.next('.custom-select');
					$select.find('option').each(function (i, option) {
						if (i === 0) return; // skip placeholder
						var $option = $(option);
						var display = $option.data('display-text') || $option.text();
						$dropdown.find('ul').append(`
						<li class="option ${$option.is(':selected') ? 'selected' : ''}"
							data-value="${$option.val()}"
							data-display-text="${display}">
						${$option.text()}
						</li>`);
					});
				}
			});
		}

		create_custom_dropdowns();

		// Toggle open
		$(document).on('click', '.custom-select', function (e) {
			$('.custom-select').not(this).removeClass('open');
			$(this).toggleClass('open');
			if ($(this).hasClass('open')) {
				$(this).find('.custom-select-search input').focus();
			}
			e.stopPropagation();
		});

		// Outside click closes dropdown
		$(document).on('click', function () {
			$('.custom-select').removeClass('open');
			$('.custom-select-search input').val('');
			$('.custom-select .option').show();
			$('.custom-select-not-found').hide();
		});

		// Select option
		$(document).on('click', '.custom-select .option', function (e) {
			var $option = $(this);
			var $dropdown = $option.closest('.custom-select');
			var value = $option.data('value');
			var text = $option.data('display-text') || $option.text();

			$dropdown.find('.option').removeClass('selected');
			$option.addClass('selected');
			$dropdown.find('.current').text(text);
			$dropdown.prev('select').val(value).trigger('change');

			$dropdown.removeClass('open');
			e.stopPropagation();
		});

		// Search
		$(document).on('input', '.custom-select-search input', function () {
			var searchText = $(this).val().toLowerCase();
			var $customSelect = $(this).closest('.custom-select');
			var found = false;

			$customSelect.find('.option').each(function () {
				var optionText = $(this).text().toLowerCase();
				var match = optionText.indexOf(searchText) !== -1;
				$(this).toggle(match);
				if (match) found = true;
			});

			$customSelect.find('.custom-select-not-found').toggle(!found);
		});
	}

	customSelect();


	$(document).on('click', '.monthselect', function () {
		console.log('.test');
	});

});
