new Vue({
        el: '#fpl',
        data: {
            apiData: undefined,
            tableData: undefined,
            selectedLeague: true,
            selectedTeam: undefined,
            showDetails: false,

            pagination: {
                sortBy: 'rank'
            },
            
            headers: [{
                    text: 'Rank',
                    align: 'left',
                    value: 'rank'
                },
                {
                    text: 'Name',
                    value: 'teamName'
                },
                {
                    text: 'Live Points',
                    value: 'livePoints'
                },
                {
                    text: 'Previous Total Points',
                    value: 'totalPoints'
                },
                {
                    text: 'New Total Points',
                    value: 'newTotalPoints'
                },
                {
                    text: 'Captain',
                    value: 'captain'
                },
                {
                    text: 'Vice Captain',
                    value: 'viceCaptain'
                }
            ]

        },
        methods: {
            loadApi: function () {
                this.$http.get('data/gw2data.json').
                then(this.successCallback, this.errorCallback);
            },
            successCallback: function (response) {
                this.apiData = response.data;
                console.log('successCallback response', this.apiData);
                this.leagueData();
            },
            errorCallback: function (response) {
                console.log('errorCallback response', response);
            },
            selectionLeagueChange: function (response) {
                console.log('selectionChanged:this.selectedLeague', this.selectedLeague);
            },
            leagueData: function () {
                //data = [["rank","teamname", "livePoints", "totalpoints", "captain", "viceCaptain"], ["teamname", "livePoints", "totalpoints", "captain", "viceCaptain"]]
                data = [];
                for (i in this.apiData) {
                    team = this.apiData[i]
                    teamData = {};
                    teamData["rank"] = team.rank;
                    teamData["teamName"] = team.entry_name;
                    teamData["livePoints"] = 0;
                    teamData["totalPoints"] = team.total;
                    teamData["newTotalPoints"] = team.total + teamData["livePoints"];
                    teamData["captain"] = "0";
                    teamData["viceCaptain"] = "0";
                    data.push(teamData);
                }

                this.tableData = data;
                console.log('loaded tableData', data);
            },
            changeSort(column) {
                //default vuetify code
                if (this.pagination.sortBy === column) {
                    this.pagination.descending = !this.pagination.descending
                } else {
                    this.pagination.sortBy = column
                    this.pagination.descending = false
                }
            }

        },
        created: function () {
            this.loadApi()
        },

    }

);
