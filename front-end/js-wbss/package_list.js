import React from 'react';
import ReactDOM from 'react-dom';

import Package from './package.js'
import AddPackage from './add_package.js'

class PackageList extends React.Component:
	constructor(props):
		super(props)

	add_pkg(selected_pkg):
		for (var i = 0; i < this.state.pkgs.length; ++i):
			let id = this.state.pkgs[i]
			if (this.global_conf[id].type === selected_pkg):
				return
		let new_id = '' + this.global_conf.next_id++
		let pkgs = this.state.pkgs.slice()
		pkgs.push(new_id)
		let pkgs_ids = Object.assign({}, this.state.pkgs_ids)
		pkgs_ids[new_id] = true
		this.global_conf[new_id] = {
			type: selected_pkg
			pkgs: []
			pkgs_ids: {}
		}
		this.conf.pkgs.push(new_id)
		this.conf.pkgs_ids[new_id] = true
		this.setState({
			pkgs: pkgs
			pkgs_ids: pkgs_ids
		})

	add_existing_pkg(id_pkg):
		for (var i = 0; i < this.state.pkgs.length; ++i):
			let id = this.state.pkgs[i]
			if (id === id_pkg):
				return
			if (this.global_conf[id].type === this.global_conf[id_pkg].type):
				return
		let pkgs = this.state.pkgs.slice()
		pkgs.push(id_pkg)
		let pkgs_ids = Object.assign({}, this.state.pkgs_ids)
		pkgs_ids[id_pkg] = true
		this.conf.pkgs.push(id_pkg)
		this.conf.pkgs_ids[id_pkg] = true
		this.setState({
			pkgs: pkgs
			pkgs_ids: pkgs_ids
		})

	render():
		let pkgs = this.props.parent.state.pkgs.map((id) => :[
			return <jsx>
				<Package
					key={id}
					s_id={id}
					parent={this.props.parent}
				/>
			</jsx>
		])
		return <jsx>
<div>
	<div>{pkgs}</div>
	<hr />
	<AddPackage
		global_conf={this.props.parent.global_conf}
		add_pkg={this.add_pkg.bind(this.props.parent)}
		add_existing_pkg={this.add_existing_pkg.bind(this.props.parent)}
	/>
</div>
		</jsx>

export { PackageList as default };
