import React from 'react';
import ReactDOM from 'react-dom';

import PackageList from './package_list.js'

class Configuration extends React.Component {
	constructor(props) {
		super(props);

		this.id = '0';
		this.id_type = null;
		this.global_conf = JSON.parse(props.conf);
		this.conf = this.global_conf[this.id];
		this.state = {
			pkgs: this.conf.pkgs,
			pkgs_ids: this.conf.pkgs_ids,
			conf_val: props.conf,
		};

		this.update_conf = this.update_conf.bind(this);
		this.copy_conf = this.copy_conf.bind(this);
	}

	update_conf() {
		let val = JSON.stringify(this.global_conf);
		this.setState({
			conf_val: val,
		});
	}
	copy_conf() {
		//https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Interact_with_the_clipboard
		/* navigator.permissions.query({name: "clipboard-write"}).then(result => {
			if (result.state == "granted" || result.state == "prompt") { */
				navigator.clipboard.writeText(this.state.conf_val).then(() => {
					console.log('Copied configuration successfully.');
				}, () => {
					console.log('Failed to copy configuration.');
				});
		/*
			}
		}); */
	}

	render() {
		return (
<div>
	<div>Configuration data:
		<textarea
			rows="1" cols="24"
			value={this.state.conf_val}
			readOnly={true}
		/>
		<button onClick={this.copy_conf} >Copy</button>
	</div>
	<hr />
	<PackageList
		parent={this}
		update_conf={this.update_conf}
	/>
</div>
		);
	}
}

ReactDOM.render(<Configuration conf={CONFIG} />, document.getElementById('root'));
