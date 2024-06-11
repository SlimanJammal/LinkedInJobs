import 'package:cv_builder/job_lists_page.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:permission_handler/permission_handler.dart';


void main() {
  runApp(CVBuilderApp());
}

class CVBuilderApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'CV Builder',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: StartupPage(),
    );
  }
}

class StartupPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'main title',
              style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 20),
            Text(
              'secondary title',
              style: TextStyle(fontSize: 24),
            ),
            SizedBox(height: 40),
            // ElevatedButton(
            //   onPressed: () {
            //     Navigator.push(
            //       context,
            //       MaterialPageRoute(builder: (context) => HomePage()),
            //     );
            //   },
            //   child: Text('Build Your CV'),
            // ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => SecondPage()),
                );
              },
              child: Text('Find Your Next Job'),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => JobsPage()),
                );
              },
              child: Text('Build Your CV'),
            ),
          ],
        ),
      ),
    );
  }
}

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  bool hasCV = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('CV Builder'),
        leading: BackButton(
          onPressed: () {
            Navigator.pop(context);
          },
        ),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text('Do you have an existing CV?'),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ElevatedButton(
                  onPressed: () {
                    setState(() {
                      hasCV = true;
                    });
                  },
                  child: Text('Yes'),
                ),
                SizedBox(width: 20),
                ElevatedButton(
                  onPressed: () {
                    setState(() {
                      hasCV = false;
                    });
                  },
                  child: Text('No'),
                ),
              ],
            ),
            if (hasCV) UploadCVForm(),
            if (!hasCV) NewCVForm(),
          ],
        ),
      ),
    );
  }
}

class UploadCVForm extends StatefulWidget {
  @override
  _UploadCVFormState createState() => _UploadCVFormState();
}

class _UploadCVFormState extends State<UploadCVForm> {
  final _jobDescriptionController = TextEditingController();

  Future<void> generateCVWithUpload() async {
    String jobDescription = _jobDescriptionController.text;
    var response = await http.post(
      Uri.parse('http://127.0.0.1:5000/generate_cv'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, dynamic>{
        'job_description': jobDescription,
        'user_info': {
          'name': 'John Doe',
          'email': 'john@example.com',
          'education': 'Bachelor of Science in Computer Science',
          'experience': '3 years of software development'
        }
      }),
    );

    if (response.statusCode == 200) {
      print('CV generated: ');
    } else {
      print('Failed to generate CV ${response.statusCode}');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Upload your CV'),
        ElevatedButton(
          onPressed: () {
            // Add file upload functionality
          },
          child: Text('Upload CV'),
        ),
        TextField(
          controller: _jobDescriptionController,
          maxLines: 5,
          decoration: InputDecoration(
            hintText: 'Job Description',
            border: OutlineInputBorder(),
          ),
        ),
        ElevatedButton(
          onPressed: generateCVWithUpload,
          child: Text('Generate CV'),
        ),
      ],
    );
  }
}

class NewCVForm extends StatefulWidget {
  @override
  _NewCVFormState createState() => _NewCVFormState();
}

class _NewCVFormState extends State<NewCVForm> {
  final _jobDescriptionController = TextEditingController();
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();
  final _educationController = TextEditingController();
  final _experienceController = TextEditingController();
  final _linkedinController = TextEditingController();
  final _githubController = TextEditingController();
  final _phoneNumberController = TextEditingController();
  final _addressController = TextEditingController();
  final _careerObjectiveController = TextEditingController();
// Education fields
  final _degreeController = TextEditingController();
  final _institutionController = TextEditingController();
  final _yearsInEducationController =
      TextEditingController(); // Assuming 'years' refers to years in education
  final _educationDetailsController = TextEditingController();

// Experience fields
  final _jobTitleController = TextEditingController();
  final _companyController = TextEditingController();
  final _locationController = TextEditingController();
  final _experienceYearsController =
      TextEditingController(); // Assuming 'years' refers to experience years
  final _responsibilitiesController = TextEditingController();

  // For skills
  final _skillsController = TextEditingController();

  // For certificates
  final _certificateNameController = TextEditingController();
  final _certificateInstitutionController = TextEditingController();
  final _certificateyearController = TextEditingController();

  // For projects
  final _projectNameController = TextEditingController();
  final _projectDescriptionController = TextEditingController();

// For awards
  final _awardNameController = TextEditingController();
  final _cawardInstitutionController = TextEditingController();
  final _awardyearController = TextEditingController();

//proffesional affeliationa
  final _orginizationNameController = TextEditingController();
  final _roleController = TextEditingController();
  final _affiliationyearController = TextEditingController();

  Future<void> generateNewCV() async {
    String jobDescription = _jobDescriptionController.text;
    String name = _nameController.text;
    String email = _emailController.text;
    String phoneNumber = _phoneNumberController.text;
    String address = _addressController.text;
    String education = _educationController.text;
    String experience = _experienceController.text;
    String linkedinProfile = _linkedinController.text;
    String githubProfile = _githubController.text;
    String careerObjective = _careerObjectiveController.text;
    String degree = _educationController.text;
    String institution = _educationController.text;
    String years = _educationController.text;
    String details = _educationController.text;

// For experience fields
    String jobTitle = _experienceController.text;
    String company = _experienceController.text;
    String location = _experienceController.text;
    String experienceYears = _experienceController
        .text; // Assuming 'years' refers to experience years
    String responsibilities = _experienceController.text;

// For skills
    String skills = _skillsController.text;

// For certificates
    String certificateName = _certificateNameController.text;
    String certificateInstitution = _certificateInstitutionController.text;
    String certificateyear = _certificateyearController.text;
// For projects
    String projectName = _projectNameController.text;
    String projectDescription = _projectDescriptionController.text;

// For awards
    String awardName = _awardNameController.text;
    String cawardInstitution = _cawardInstitutionController.text;
    String awardyear = _awardyearController.text;

//proffesional affeliationa
    String orginizationName = _orginizationNameController.text;
    String role = _roleController.text;
    String affiliationyear = _affiliationyearController.text;

    var response = await http.post(
      Uri.parse('http://127.0.0.1:5000/generate_cv'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, dynamic>{
        "job_description": jobDescription,
        "user_info": {
          "full_name": name,
          "email": email,
          "phone": phoneNumber,
          "address": address,
          "linkedin": linkedinProfile,
          "career_objective":
              "To obtain a Software Engineer position at a reputable tech company...",
          "education": [
            {
              "degree": "B.Sc. in Computer Science",
              "institution": "University of Example",
              "years": "2015-2019",
              "details": "Graduated with honors..."
            },
            {
              "degree": "M.Sc. in Software Engineering",
              "institution": "Example Institute of Technology",
              "years": "2019-2021",
              "details": "Thesis on machine learning algorithms..."
            }
          ],
          "work_experience": [
            {
              "job_title": "Software Developer",
              "company": "Tech Solutions Inc.",
              "location": "Example City",
              "years": "2021-Present",
              "responsibilities":
                  "Developed web applications using .NET and AngularJS..."
            }
          ],
          "skills": [
            "Python",
            "JavaScript",
            "React",
            "Machine Learning",
            "Project Management"
          ],
          "certifications": [
            {
              "name": "Certified Scrum Master",
              "institution": "Scrum Alliance",
              "year": "2022"
            }
          ],
          "projects": [
            {
              "name": "Personal Portfolio Website",
              "description":
                  "Designed and developed a personal portfolio website using React and Node.js..."
            },
            {
              "name": "Machine Learning Model for Predicting Stock Prices",
              "description":
                  "Developed a predictive model using Python and scikit-learn..."
            }
          ],
          "awards": [
            {
              "name": "Dean's List",
              "institution": "University of Example",
              "year": "2019"
            }
          ],
          "professional_affiliations": [
            {"organization": "IEEE", "role": "Member", "years": "2020-Present"}
          ],
          "references": []
        }
      }),
    );

    if (response.statusCode == 200) {
      print('CV generated: ${response.body}');
    } else {
      print('Failed to generate CV ${response.statusCode}');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Many Text Fields'),
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            SizedBox(height: 28),
            SizedBox(
              width: 500,
              child: TextField(
                controller: _nameController,
                decoration: InputDecoration(
                  hintText: 'Name',
                  border: OutlineInputBorder(),
                ),
              ),
            ),
            SizedBox(height: 8),
            SizedBox(
              width: 500,
              child: TextField(
                controller: _emailController,
                decoration: InputDecoration(
                  hintText: 'Email',
                  border: OutlineInputBorder(),
                ),
              ),
            ),
            SizedBox(height: 8),
            SizedBox(
              width: 500,
              child: TextField(
                controller: _educationController,
                decoration: InputDecoration(
                  hintText: 'Education',
                  border: OutlineInputBorder(),
                ),
              ),
            ),
            SizedBox(height: 8),
            SizedBox(
              width: 500,
              child: TextField(
                controller: _experienceController,
                decoration: InputDecoration(
                  hintText: 'Experience',
                  border: OutlineInputBorder(),
                ),
              ),
            ),
            SizedBox(height: 8),
            SizedBox(
              width: 500,
              child: TextField(
                controller: _linkedinController,
                decoration: InputDecoration(
                  hintText: 'Linked in Profile',
                  border: OutlineInputBorder(),
                ),
              ),
            ),
            SizedBox(height: 8),
            SizedBox(
              width: 500,
              child: TextField(
                controller: _githubController,
                decoration: InputDecoration(
                  hintText: 'Github Profile',
                  border: OutlineInputBorder(),
                ),
              ),
            ),
            SizedBox(height: 8),
            SizedBox(
              width: 500,
              child: TextField(
                controller: _jobDescriptionController,
                maxLines: 5,
                decoration: InputDecoration(
                  hintText: 'Job Description',
                  border: OutlineInputBorder(),
                ),
              ),
            ),
            SizedBox(height: 16),
            ElevatedButton(
              onPressed: generateNewCV,
              child: Text('Generate CV'),
            ),
          ],
        ),
      ),
    );
  }
}

class SecondPage extends StatefulWidget {
  @override
  _SecondPageState createState() => _SecondPageState();
}

class _SecondPageState extends State<SecondPage> with SingleTickerProviderStateMixin {
  List<Map<String, dynamic>> _jobs = []; // List to store fetched jobs
  bool _showRemoteOnly = false; // Flag to control remote job filtering
  TabController? _tabController; // TabController to manage tab changes

  final List<String> _jobTypes = ["CS", "ME", "EE"];

  Future<void> _fetchJobs(String jobType) async {
    // final response = await http.post(Uri.parse(
    //     "https://projectflaskserver.pythonanywhere.com/get_jobs?job_type=$jobType")); // Replace with your actual API endpoint
    final response = await http.post(Uri.parse(
        "http://127.0.0.1:5000/get_jobs?job_type=$jobType")); // Replace with your actual API endpoint
    if (response.statusCode == 200) {
      final jobs = jsonDecode(response.body) as List<dynamic>;
      setState(() {
        _jobs = jobs.map((job) => job as Map<String, dynamic>).toList();
      });
    } else {
      // Handle API error (e.g., display an error message)
      print("Error fetching jobs: ${response.statusCode}");
    }
  }

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
    _tabController!.addListener(_handleTabSelection);
    _fetchJobs(_jobTypes[0]); // Call _fetchJobs with the first endpoint on initialization
  }

  void _handleTabSelection() {
    if (_tabController!.indexIsChanging) {
      _fetchJobs(_jobTypes[_tabController!.index]); // Fetch jobs based on selected tab
    }
  }

  @override
  void dispose() {
    _tabController?.dispose(); // Dispose the TabController
    super.dispose();
  }


  @override
  Widget build(BuildContext context) {

    return DefaultTabController(
      length: 3,
      child: Scaffold(
        appBar: AppBar(
          title: Text('Jobs'),
          leading: BackButton(
            onPressed: () => Navigator.pop(context),
          ),
          bottom: TabBar(
            controller: _tabController,
            indicatorSize: TabBarIndicatorSize.tab,
            indicator: BoxDecoration(
              color: Colors.lightGreenAccent,
              borderRadius: BorderRadius.circular(20)
            ),
             tabs: [
               Tab(icon: Icon(Icons.code),child: Text("Software"),),
               Tab(icon: Icon(Icons.airplanemode_on_sharp),child: Text("Mechanical"),),
               Tab(icon: Icon(Icons.computer_outlined),child: Text("Hardware"),)
             ],
          ),
        ),
        body: Column(
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                Text('Show no experience jobs Only',),
                Switch(
                  value: _showRemoteOnly,
                  onChanged: (value) => setState(() => _showRemoteOnly = value),
                ),
              ],
            ),
            // List of jobs
            _jobs.isEmpty
                ? Center(
                    child:
                        Text("currently no jobs to show "))
                        //CircularProgressIndicator()) // Show loading indicator while fetching
                : Expanded(
                    child: ListView.builder(
                      itemCount: _showRemoteOnly
                          ? _jobs.where((job) => job['Needs Experience']).length
                          : _jobs.length, // Filter if needed
                      itemBuilder: (context, index) {
                        final job = _jobs[index];
                        if (_showRemoteOnly && job['Needs Experience'])
                          return Container(); // Skip non-remote jobs in filtered view
                        return Card(
                          child: Padding(
                            padding: EdgeInsets.all(16.0),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment
                                  .start, // Align text to left
                              children: [
                                Text(
                                  job['Job Title'],
                                  style: TextStyle(
                                      fontSize: 18.0,
                                      fontWeight: FontWeight.bold),
                                ),
                                SizedBox(height: 8.0), // Add spacing
                                Text(
                                    '${job['Company Name']} - ${job['Location']}',
                                    style: TextStyle(fontSize: 16.0)),
                                SizedBox(height: 8.0),
                                Text('Posted: ${job['When Posted']}',
                                    style: TextStyle(fontSize: 14.0)),
                                SizedBox(height: 8.0),
                                Row(
                                  children: [
                                    Text('Applicants: ${job['Applicants']}',
                                        style: TextStyle(fontSize: 14.0)),
                                    Spacer(), // Add space between elements
                                    Icon(
                                      job['Is Remote']
                                          ? Icons.home
                                          : Icons.location_on,
                                      color: job['Is Remote']
                                          ? Colors.blue
                                          : Colors.grey,
                                    ),
                                    Text(job['Is Remote']
                                        ? 'Hybrid'
                                        : 'On-site'),
                                  ],
                                ),
                                SizedBox(height: 8.0),
                                Row(
                                  children: [
                                    Text(
                                        'Years of Experience required: ${job['Years Experience']}',
                                        style: TextStyle(fontSize: 14.0)),
                                  ],
                                ),
                                Row(

                                  children: [
                                    FittedBox(
                                      child: Text(softWrap: true,
                                          job['Needs Experience'] != null
                                              ? 'Estimated Salary: ${job['Salary estimate']}'
                                              : 'No Salary estimate found',
                                          style: TextStyle(fontSize: 14.0)),
                                      fit: BoxFit.scaleDown,
                                    )

                                  ],
                                ),
                              ],
                            ),
                          ),
                        );
                      },
                    ),
                  ),
          ],
        ),
      ),
    );
  }
}
