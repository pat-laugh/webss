import React from 'react';
import ReactDOM from 'react-dom';

import PackageList from './package_list.js'

const langs_names = {
	'js': 'JavaScript'
	'py': 'Python'
	'wbss': 'WebSS'
};
const details_types = {
	'start_char': 'text'
	'end_char': 'text'
	'consume_end': 'checkbox'
};

class PackageConf extends React.Component:
	constructor(props):
		super(props)
		this.state = {
			is_active: props.is_active
			selected_lang: props.selected_lang
		}
		this.name = props.name
		this.desc = props.desc
		this.langs = props.langs

	render():
		let opts = []
		var key
		let langs = Object.assign({}, this.props.langs)
		for (key in langs):
			opts.push(
				<jsx><option key={key} value={key}>{langs_names[key]}</option></jsx>
			)

		let details = []
		for (var key in details_types):
			let type = details_types[key]
			let value_or_checked = langs[this.props.selected_lang][key]
			let is_checkbox = type === 'checkbox'

			# https://stackoverflow.com/a/31164357
			let input_props = {}
			if (is_checkbox):
				input_props.checked = value_or_checked
				input_props.disabled = true
			else:
				input_props.value = value_or_checked
				input_props.readOnly = true
			
			details.push(<jsx>
			<label key={key}>
				<span>{key}:</span>
				<span>
					<input 
						type={details_types[key]}
						name={key}
						{...input_props}
					/>
				</span>
			</label>
			</jsx>)
				
		return <jsx>
<div className="package-conf">
	<span className="package-conf-text">Configuration:
		<select
			value={this.props.selected_lang}
			onChange={this.props.set_selected_lang}
		>
			{opts}
		</select>
	</span>
	<details className="package-conf-details">
		<summary>Show details</summary>
		<div className="package-conf-details-list">
			{details}
		</div>
	</details>
</div>
		</jsx>

class Package extends React.Component:
	constructor(props):
		super(props)

		this.id = props.s_id
		this.parent = props.parent
		this.update_conf = this.parent.update_conf

		this.global_conf = this.parent.global_conf
		this.conf = this.global_conf[this.id]

		this.id_type = this.global_conf[this.id].type
		const data = ALL_PKGS[this.id_type]
		this.name = data.name
		this.desc = data.desc
		this.langs = data.langs

		this.state = {
			is_active: this.parent.conf.pkgs_ids[this.id]
			pkgs: this.conf.pkgs
			pkgs_ids: this.conf.pkgs_ids
			selected_lang: data.selected_lang
			over: false
			show_packages: false
			show_details: false
			load_packages: false
			load_details: false
		}

		this.set_active = this.set_active.bind(this)
		this.set_selected_lang = this.set_selected_lang.bind(this)
		this.handle_on_over = this.handle_on_over.bind(this)
		this.handle_on_out = this.handle_on_out.bind(this)
		this.handle_on_leave = this.handle_on_leave.bind(this)
		this.toggle_show_packages = this.toggle_show_packages.bind(this)
		this.toggle_show_details = this.toggle_show_details.bind(this)
		this.ignore_leave = false

		this.update_conf()
	set_selected_lang(e):
		this.setState({
			selected_lang: e.target.value
		})
	set_active(e):
		let is_active = e.target.checked
		this.setState({
			is_active: is_active
		})
		this.parent.conf.pkgs_ids[this.id] = is_active
		this.update_conf()
	handle_on_over(e):
		if (e.target.tagName.toLowerCase() === 'select'):
			this.ignore_leave = true
			e.stopPropagation()
		e.stopPropagation()
		# e.currentTarget.children[0].classList.add('package-over')
		###
		this.setState({
			over: true
			right_over: true
		})
		let items = document.getElementsByClassName('pkg-id-' + this.id)
		for (var i = 0; i < items.length; ++i):
			let item = items[i]
			item.classList.add('package-over')
	handle_on_out(e):
		if (e.target.tagName.toLowerCase() === 'select'):
			this.ignore_leave = false
			return
		# e.stopPropagation()
		# e.currentTarget.children[0].classList.remove('package-over')
		###
		this.setState({
			right_over: false
		})
		let items = document.getElementsByClassName('pkg-id-' + this.id)
		for (var i = 0; i < items.length; ++i):
			let item = items[i]
			item.classList.remove('package-over')
	handle_on_leave(e):
		if (e.target.tagName.toLowerCase() === 'select'):
			this.ignore_leave = false
			return
		this.setState({
			over: false
		})
	toggle_show_packages(e):
		e.preventDefault()
		this.setState({
			show_packages: !this.state.show_packages
			load_packages: this.state.load_packages || !this.state.show_packages
		})
	toggle_show_details(e):
		e.preventDefault()
		this.setState({
			show_details: !this.state.show_details
			load_details: this.state.load_details || !this.state.show_details
		})

	render():
		let cls_name = 'package-in'
		cls_name += ' package-active-' + (this.state.is_active ? '1' : '0')
		cls_name += ' pkg-id-' + this.id
		if (this.state.over):
			cls_name += ' package-over'
		return <jsx>
<div
	className="package-out"
	onMouseOver={this.handle_on_over}
	onMouseOut={this.handle_on_out}
	onMouseLeave={this.handle_on_leave}
>
<div
	className={cls_name}
>
	<label className="package-text">
		<input type="checkbox"
			name="is_active"
			checked={this.state.is_active}
			onChange={this.set_active}
		/>
		<span className="package-name">#{this.id} - {this.name}</span>
	</label>
	{!(this.state.right_over || this.state.show_details) ? '' : (
	<details
		className="package-details"
		open={this.state.show_details}
	>
		<summary
			onClick={this.toggle_show_details}
		>Show details</summary>
		{this.state.load_details ? (
		<span>
			<div className="package-desc">{this.desc}</div>
			<PackageConf
				langs={this.langs}
				selected_lang={this.state.selected_lang}
				set_selected_lang={this.set_selected_lang}
			/>
		</span>) : ''}
	</details>
	)}
	{!(this.state.over || this.state.show_packages) ? '' : (
	<details
		open={this.state.show_packages}
	>
		<summary
			onClick={this.toggle_show_packages}
		>Show packages ({this.state.pkgs.length})</summary>
		{this.state.load_packages ? (
	<PackageList
		parent={this}
		update_conf={this.update_conf}
	/>) : ''}
	</details>
	)}
</div>
</div>
		</jsx>

export { Package as default };
