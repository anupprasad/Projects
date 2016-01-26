var IndexModule = angular.module('IndexModule', ['ngSanitize']);

/*IndexModule.factory('IndexLoadService',['$scope', '$http',function($scope,$http)
{
	
	return {
		jsonData : function()
		{
			$http.get('js/'+$scope.page+'.json').success(function(data) {
            $scope.artists = data;
            });
		}
	}
}]);*/


IndexModule.factory('IndexLoadService', function() {
	return {
		jsonData : function($attrs,$scope,$http,$templateCache)
		{
            var path='';
            if(!$scope.initialize)
                {
                    $http.get('assets/Json/initialize.json',{cache: $templateCache}).success(function(data) {
                  $scope.initialize=data;
                });
                }
               
          if($attrs.class==='Introduction')
              {
                  if(!$scope.profile)
                  {
                  path='assets/Json/Index.json';
                  $http.get(path,{cache: $templateCache}).success(function(data) {
                  $scope.profile=data;});
                  }
            }
            else if($attrs.class==='Education')
                {
                  if(!$scope.edu)
                  {
                  path='assets/Json/education.json';
                  $http.get(path,{cache: $templateCache}).success(function(data) {
                  $scope.edu=data;});
                  }
                }
            else if($attrs.class==='Expertise')
                {
                  if(!$scope.edu)
                  {
                  path='assets/Json/experties.json';
                  $http.get(path,{cache: $templateCache}).success(function(data) {
                  $scope.expert=data;});
                  }
                }
             else if($attrs.class==='Projects')
                {
                  if(!$scope.project)
                  {
                  path='assets/Json/projects.json';
                  $http.get(path,{cache: $templateCache}).success(function(data) {
                  $scope.project=data;});
                  }
                }
            
             else if($attrs.class==='Certification')
                {
                  if(!$scope.certi)
                  {
                  path='assets/Json/certificate.json';
                  $http.get(path,{cache: $templateCache}).success(function(data) {
                  $scope.certi=data;});
                  }
                }
             else if($attrs.class==='Work Experience')
                {
                  if(!$scope.workex)
                  {
                  path='assets/Json/WorkExperiance.json';
                  $http.get(path,{cache: $templateCache}).success(function(data) {
                  $scope.workex=data;});
                  }
                }
            else if($attrs.class==='Research Work')
                {
                  if(!$scope.rwork)
                  {
                  path='assets/Json/research.json';
                  $http.get(path,{cache: $templateCache}).success(function(data) {
                  $scope.rwork=data;});
                  }
                }
            else if($attrs.class==='Coding Challenges')
                {
                  if(!$scope.codec)
                  {
                  path='assets/Json/codechallenge.json';
                  $http.get(path,{cache: $templateCache}).success(function(data) {
                  $scope.codec=data;});
                  }
                }
              else if($attrs.class==='Resume')
                {
                  if(!$scope.resume)
                  {
                  path='assets/Json/resume.json';
                  $http.get(path,{cache: $templateCache}).success(function(data) {
                  $scope.resume=data;});
                  }
                }
            
		}
	}
});





IndexModule.controller('IndexController', ['$http','$attrs','$scope','$templateCache','IndexLoadService', function($http,$attrs,$scope,$templateCache,IndexLoadService) {
     IndexLoadService.jsonData($attrs,$scope,$http,$templateCache);
    $scope.active=$attrs.class;
    }]);


/*IndexModule.controller('IndexController', ["$scope","$http", "$attrs",function($scope,$http,$attrs) {
     var jsonToLoad=$attrs.class;
    if(jsonToLoad=="")
     $http.get('js/'+$scope.page+'.json').success(function(data) {
            $scope.artists = data;
            });
    }]);*/


/*IndexModule.directive('IndexDirective', function() {
return {SSSS
restrict: 'A',
scope: {
myUrl: '@', // binding strategy
},
controller:
var value=$scope.myUrl;
}
})*/