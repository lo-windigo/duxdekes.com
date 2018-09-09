

$(function() {

	states = {
		"AK": "Alaska",
		"AL": "Alabama",
		"AR": "Arkansas",
		"AS": "American Samoa",
		"AZ": "Arizona",
		"CA": "California",
		"CO": "Colorado",
		"CT": "Connecticut",
		"DC": "District of Columbia",
		"DE": "Delaware",
		"FL": "Florida",
		"FM": "Federated States of Micronesia",
		"GA": "Georgia",
		"GU": "Guam",
		"HI": "Hawaii",
		"IA": "Iowa",
		"ID": "Idaho",
		"IL": "Illinois",
		"IN": "Indiana",
		"KS": "Kansas",
		"KY": "Kentucky",
		"LA": "Louisiana",
		"MA": "Massachusetts",
		"MD": "Maryland",
		"ME": "Maine",
		"MH": "Marshall Islands",
		"MI": "Michigan",
		"MN": "Minnesota",
		"MO": "Missouri",
		"MP": "Northern Mariana Islands",
		"MS": "Mississippi",
		"MT": "Montana",
		"NC": "North Carolina",
		"ND": "North Dakota",
		"NE": "Nebraska",
		"NH": "New Hampshire",
		"NJ": "New Jersey",
		"NM": "New Mexico",
		"NV": "Nevada",
		"NY": "New York",
		"OH": "Ohio",
		"OK": "Oklahoma",
		"OR": "Oregon",
		"PA": "Pennsylvania",
		"PR": "Puerto Rico",
		"PW": "Palau",
		"RI": "Rhode Island",
		"SC": "South Carolina",
		"SD": "South Dakota",
		"TN": "Tennessee",
		"TX": "Texas",
		"UT": "Utah",
		"VA": "Virginia",
		"VI": "Virgin Islands",
		"VT": "Vermont",
		"WA": "Washington",
		"WI": "Wisconsin",
		"WV": "West Virginia",
		"WY": "Wyoming"
	}

	country_dropdown = $('#id_country');
	state_dropdown = $('<select></select>', {
		id: 'id_state',
		class: 'form-control',
		name: 'state'
	});
	state_text = $('#id_state');

	$.each(states, function(postal, state) {
		state_dropdown.append($('<option></option>', {
			'value': postal,
			'text': state
		}));
	});

	// Change the state/county field to a US-appropriate one if that country is
	// selected
	function countryChange() {
		current_field = $('#id_state')
		current_value = current_field.val()

		if(country_dropdown.val() == 'US') {

			if(!current_value) {
				current_value = 'NY'
			}

			state_dropdown.val(current_value);
			current_field.replaceWith(state_dropdown);
		}
		else {
			current_field.replaceWith(state_text);
		}
	}

	// Attach the countryChange event handler to the country dropdown
	country_dropdown.change(countryChange);
	
	// Run this once to make sure the field is presented correctly
	countryChange();
});
