var React = require('react');
var DataTable = require('react-data-components').DataTable;
var d3 = require('d3');

var BookTableRow = React.createClass({
    displayName: "HouseRow",
    render: function() {
        return (
            <tr>
                <td>{this.props.house.postcode}</td>
                <td>{this.props.house.vraagprijs}</td>
            </tr>
        );
    },
});

//

var BookTable = React.createClass({
    displayName: "HouseTable",
    render: function() {
        var rows = [];
        this.props.houses.forEach(function(house) {
            rows.push(<BookTableRow key={house.id} house={house} />);
        }.bind(this));
        return (
            <table>
                <thead>
                    <tr>
                        <th>Adres</th>
                        <th>Vraagprijs</th>
                    </tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>
        );
    }
});

var BookPanel = React.createClass({
    displayName: "HousePanel",
    getInitialState: function() {
        return {
            houses: [],
        };
    },
    render: function() {
        return(
            <div className="row">
                <div className="one-half column">
                    <BookTable houses={this.state.houses} />
                </div>
            </div>
        );
    },
    componentDidMount: function() {
        this.reloadBooks('');
    },
    reloadBooks: function(query) {
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            cache: false,
            success: function(data) {
                this.setState({
                    houses: data,

                });
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.url, status, err.toString());
                this.setState({
                    message: err.toString()
                });
            }.bind(this)
        });
    },
});

function buildTable(data) {
  //var renderMapUrl =
  //  (val, row) =>
  //    <a href={`https://www.google.com/maps?q=${row['LAT']},${row['LON']}`}>
  //      Google Maps
  //    </a>;

  var tableColumns = [
    { title: 'id', prop: 'id' },
    { title: 'fuid', prop: 'fuid' },
    { title: 'postcode', prop: 'postcode' },
    { title: 'vraagprijs', prop: 'vraagprijs' },
    //{ title: 'link', prop: 'link' },
    //{ title: 'Phone', prop: 'PHONE NUMBER', defaultContent: '<no phone>' },
    //{ title: 'Map', render: renderMapUrl, className: 'text-center' },
  ];

  return (
    <DataTable
      className="cont"
      keys={[ 'id', 'fuid', 'postcode', 'vraagprijs' ]}
      columns={tableColumns}
      initialData={data}
      initialPageLength={5}
      initialSortBy={{ prop: 'id', order: 'descending' }}
      pageLengthOptions={[ 5, 20, 50 ]}
    />
  );
}



d3.json(url='/api/houses/', function(error, rows) {
  React.render(buildTable(rows), document.getElementById('root'));
});

React.render(<BookPanel url='/api/houses/' />, document.getElementById('content'));