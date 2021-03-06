let statesAndCounties = {}
let stateSelect = $('select#state')
let countySelect = $('select#county')
let iframe = $('iframe')

let lastState, currentState
let selectCounty = '<option selected disabled>--Select a County--</option>'
stateSelect.change(function() {
	currentState = stateSelect.val()
	if (currentState !== lastState) {
		lastState = currentState

		iframe.attr('src', currentState + '.html')

		countySelect.empty()
		countySelect.append(selectCounty)
		statesAndCounties[currentState].forEach(function(county) {
			countySelect.append('<option value="' + county + '">' + county + '</option>')
		})
		console.log(currentState)	
	}
})

let lastCounty, currentCounty
countySelect.change(function() {
	currentCounty = countySelect.val()
	if (currentCounty !== lastCounty) {
		lastCounty = currentCounty

		iframe.attr('src', currentState + '/' + currentCounty + '.html')

		console.log(currentCounty)
	}
})

$.getJSON('states_and_counties.json')
	.done(function(data) {
		$('p').text('updated at: ' + data.updated_at)
		statesAndCounties = data.states_and_counties
		Object.keys(statesAndCounties).forEach(function(state) {
			stateSelect.append('<option value="' + state + '">' + state + '</option>')
		})
	})
