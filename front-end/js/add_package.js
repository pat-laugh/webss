import React from 'react';
import ReactDOM from 'react-dom';

class AddPackage extends React.Component {
	constructor(props) {
		super(props);

		let pkgs_ids_names = [];
		for (var key in ALL_PKGS)
			pkgs_ids_names.push([key, ALL_PKGS[key].name]);
		pkgs_ids_names.sort((a, b) => b[1].toLowerCase() < a[1].toLowerCase());
		this.pkgs_ids_names = pkgs_ids_names;

		this.global_conf = props.global_conf;
		let id_existing_pkg = '';
		for (var key in this.global_conf) {
			if (key === '0' || key === 'next_id')
				continue;
			id_existing_pkg = key;
			break;
		}
		this.state = {
			selected_pkg: pkgs_ids_names[0][0],
			selected_existing_pkg: id_existing_pkg,
		};

		this.set_selected_pkg = this.set_selected_pkg.bind(this);
		this.set_selected_existing_pkg = this.set_selected_existing_pkg.bind(this);
	}

	set_selected_pkg(e) {
		this.setState({
			selected_pkg: e.target.value,
		});
	}
	set_selected_existing_pkg(e) {
		this.setState({
			selected_existing_pkg: e.target.value,
		});
	}

	render() {
		let opts = [];
		for (var i = 0; i < this.pkgs_ids_names.length; ++i) {
			const [id, name] = this.pkgs_ids_names[i];
			opts.push(
				<option key={id} value={id}>{name}</option>
			);
		}
		let opts_existing = [];
		for (var key in this.global_conf) {
			if (key === '0' || key === 'next_id')
				continue;
			opts_existing.push(
				<option key={key} value={key}>#{key}</option>
			);
		}
		return (
<div>
	<fieldset>
	<select
		value={this.state.selected_pkg}
		onChange={this.set_selected_pkg}
	>{opts}</select>
	<button onClick={(e) => { this.props.add_pkg(this.state.selected_pkg); }} >Add package</button>
	</fieldset>
	<fieldset>
	<select
		value={this.state.selected_existing_pkg}
		onChange={this.set_selected_existing_pkg}
	>{opts_existing}</select>
	<button
		onClick={(e) => { this.props.add_existing_pkg(this.state.selected_existing_pkg); }}
	>Add existing package</button>
	</fieldset>
</div>
		);
	}
}

export { AddPackage as default };
