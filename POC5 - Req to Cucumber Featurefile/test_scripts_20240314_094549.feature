:

Feature: Document File Operations

Scenario: Create new empty document

Given the application is open
And the user is on the home page
When the user clicks on the "New Document" button
Then a blank document is created with the title "Untitled"
And the application displays a message "Document created successfully"

Scenario Outline: Create new empty document with invalid input
Given the application is open
And the user is on the home page
When the user enters "<invalid input>" in the "New Document" field
And the user clicks on the "New Document" button
Then the application displays an error message "Invalid input, please enter a valid document name"

Examples:
|invalid input|
|"      "     |
|"$$%^&*"     |
|""           |

Scenario: Save current document before closing
Given the application is open
And the user has unsaved changes in their document
When the user clicks on the "Close" button
Then the application displays a dialog box asking if the user wants to save their changes
And the user clicks on the "Save" button
Then the changes are saved and the document is closed

Scenario Outline: Save current document with invalid input
Given the application is open
And the user has unsaved changes in their document
When the user enters "<invalid input>" in the "Save" field
And the user clicks on the "Save" button
Then the application displays an error message "Invalid input, please enter a valid file name"

Examples:
|invalid input|
|"      "     |
|"$$%^&*"     |
|""           |

Scenario: Open document from chosen file
Given the application is open
And the user is on the home page
When the user clicks on the "Open Document" button
Then the user is prompted to choose a file from their computer
And the selected document is opened in the application

Scenario: Save opened document into a file
Given the application is open
And a document is currently opened
When the user clicks on the "Save Document" button
Then the document is saved with the original file name
And the application displays a message "Document saved successfully"

Scenario: Create document template file from opened document
Given the application is open
And a document is currently opened
When the user clicks on the "Create Template" button
Then a document template file is generated with the same structure and attribute values as the opened document
And the application displays a message "Template created successfully"

Scenario: Create new document from chosen template file
Given the application is open
And the user is on the home page
When the user clicks on the "New Document from Template" button
Then the user is prompted to choose a template file from their computer
And a new document is created with the same structure and attribute values as the template file
And the application displays a message "Document created from template successfully"

Scenario: Import MS Word document
Given the application is open
And the user is on the home page
When the user clicks on the "Import Word Document" button
Then the user is prompted to choose a Word document from their computer
And the document is imported into the application, preserving structure, rich text description, and images
And the application displays a message "Document imported successfully"

Scenario: Import MS Excel table of requirements
Given the application is open
And the user is on the home page
When the user clicks on the "Import Excel Table" button
Then the user is prompted to choose an Excel file from their computer
And the table of requirements is imported into the application, preserving headings, levels, unformatted text description, and custom attribute values
And the application displays a message "Table of requirements imported successfully"

Scenario: Export document view to HTML
Given the application is open
And a document is currently opened
When the user clicks on the "Export to HTML" button
Then the document view is exported to an HTML file
And the application displays a message "Document view exported to HTML successfully"

Scenario: Export requirements to CSV
Given the application is open
And a document is currently opened
When the user clicks on the "Export to CSV" button
Then the requirements are exported to a CSV file
And the application displays a message "Requirements exported to CSV successfully"

Feature: Document View

Scenario: Display table of contents
Given a document is currently opened
When the user clicks on the "Table of Contents" button
Then the application displays a table of contents, organized according to the document hierarchy
And when the user clicks on a section in the table of contents, the corresponding section is focused in the requirements table

Scenario: Change width of requirements table columns
Given a document is currently opened
When the user clicks and drags on the edge of a column header in the requirements table
Then the column width is adjusted to match the user's input

Scenario: Reorder requirements table columns
Given a document is currently opened
When the user clicks on a column header in the requirements table
Then the columns are rearranged in the order selected by the user

Scenario: Show and hide requirements table columns
Given a document is currently opened
When the user clicks on the "Show/Hide Columns" button
Then a list of available columns is displayed
And when the user clicks on a column name, that column is shown or hidden in the requirements table

Scenario: Sort requirements table columns
Given a document is currently opened
When the user clicks on the column header of a sortable column
Then the requirements in the table are sorted in ascending or descending order based on that column

Scenario: Show and hide detailed information pane
Given a document is currently opened
When the user clicks on a requirement in the requirements table
Then a pane is displayed with detailed information about that requirement, including custom attributes, discussion, traceability links, and history of changes
And when the user clicks on the "Hide Pane" button, the pane is hidden from view

Feature: Performance Testing

Scenario: Open large document
Given the application is open
And a document with over 1000 requirements is currently opened
When the document is loaded
Then the application should not crash or freeze
And the document should be displayed without any lag

Scenario: Save large document
Given the application is open
And a document with over 1000 requirements is currently opened
When the document is saved
Then the application should not crash
And the save process should not take longer than a specified amount of time

Scenario: Import large MS Word document
Given the application is open
And the user has a large Word document with over 1000 requirements
When the user imports this document
Then the application should not crash or freeze
And the document should be imported without any lag

Scenario: Import large MS Excel table of requirements
Given the application is open
And the user has a large Excel table with over 1000 requirements
When the user imports this table
Then the application should not crash or freeze
And the table of requirements should be imported without any lag

Feature: Requirements Table Functionality

Scenario: Display of Requirement Comments
Given The user is on the Requirements Table page
When The user views the requirements table
Then The requirement comments should be displayed
And The comments should have the following information:
| Author | Date | Text |
| Comment 1 | 01/01/2020 | This is comment 1 |
| Comment 2 | 02/01/2020 | This is comment 2 |

Scenario: Display of Requirement Comments Ordered by Date and Time
Given The user is on the Requirements Table page
When The user views the requirement comments
Then The comments should be ordered by date and time in ascending order

Scenario: Display of Requirement Traceability Links
Given The user is on the Requirements Table page
When The user views the requirements table
Then The Links column should be displayed
And The links should be grouped by link types

Scenario: Change Width of Requirements Table Columns
Given The user is on the Requirements Table page
When The user resizes a column in the table
Then The width of the column should be changed accordingly

Scenario: Reordering Requirements Table Columns
Given The user is on the Requirements Table page
When The user drags and drops a column to a new position
Then The columns in the table should be reordered accordingly

Scenario: Show and Hide Requirements Table Columns
Given The user is on the Requirements Table page
When The user selects a column to show or hide
Then The selected column should be displayed or hidden
And The ID column should always be shown and cannot be hidden

Scenario: Sorting of Requirements Table Columns
Given The user is on the Requirements Table page
When The user clicks on a column header
Then The table should be sorted in ascending or descending order based on the selected column
And The Discussion and Links columns should not be sortable

Scenario: Display of Detailed Information Pane
Given The user is on the Requirements Table page
When The user selects to display detailed information pane
Then The selected requirement's details should be displayed in the pane
And The following options should be available in the pane:
| Custom Attributes | Discussion | Traceability Links | History of Changes |

Scenario: Display of Custom Attributes in the Custom Attributes Pane
Given The user is on the Detailed Information Pane for a selected requirement
When The user views the Custom Attributes Pane
Then The values of all assigned custom attributes should be displayed

Scenario: Display of Comments in the Discussion Pane
Given The user is on the Detailed Information Pane for a selected requirement
When The user views the Discussion Pane
Then All comments for the selected requirement should be displayed
And The comments should be ordered by date and time

Scenario: Expand and Collapse Comments in the Discussion Pane
Given The user is on the Discussion Pane for a selected requirement
When The user clicks on a comment or the option to expand or collapse all comments
Then The selected or all comments should be expanded or collapsed accordingly

Scenario: Display of Comment Details
Given The user is on the Discussion Pane for a selected requirement
When The user expands a comment
Then The date, time, author, and description of the comment should be displayed

Scenario: Collapse of Comment Details
Given The user is on the Discussion Pane for a selected requirement
When The user collapses a comment
Then The date, time, and author of the comment should be displayed

Scenario: Display of Traceability Links in the Links Pane
Given The user is on the Detailed Information Pane for a selected requirement
When The user views the Links Pane
Then All traceability links starting in or leading to the selected requirement should be displayed
And The links should be grouped by link types
And The links should be ordered by ID of the linked object

Scenario: Focus on Linked Requirement
Given The user is on the Links Pane for a selected requirement
When The user clicks on a traceability link
Then The linked requirement should be focused on

Scenario: Creating a New Requirement
Given The user is on the Requirements Table page
When The user creates a new requirement and places it in a document section
Then The new requirement should have a unique and unchangeable ID assigned to it

Scenario: Copying Requirements or Document Sections
Given The user is on the Requirements Table page
When The user selects and copies requirements or document sections
Then The selected requirements or document sections should be copied

Scenario: Moving Requirements or Document Sections
Given The user is on the Requirements Table page
When The user selects and moves requirements or document sections to a new position
Then The selected requirements or document sections should be moved accordingly

Scenario: Marking Requirements or Document Sections as Deleted
Given The user is on the Requirements Table page
When The user selects and marks requirements or document sections as deleted
Then The selected requirements or document sections should be marked as deleted

Scenario: Undeleting Previously Deleted Requirements or Document Sections
Given The user is on the Requirements Table page
When The user selects and undoes a previously deleted requirement or document section
Then The selected requirement or document section should be restored

Scenario: Permanently Removing Deleted Requirements or Document Sections
Given The user is on the Requirements Table page
When The user selects and permanently removes a deleted requirement or document section
Then The selected requirement or document section should be permanently removed

Scenario: Editing Heading of a Section
Given The user is on the Requirements Table page
When The user edits the heading of a section
Then The heading of the section should be changed accordingly

Scenario: Editing Text Description of a Requirement
Given The user is on the Requirements Table page
When The user edits the text description of a requirement
Then The text description of the requirement should be changed accordingly

Scenario: Pasting HTML Content from MS Word, Excel, or Other Applications into a Requirement Text Description
Given The user has copied HTML content from MS Word, Excel, or other application
And The user is on the Requirements Table page
When The user pastes the HTML content into a requirement text description
Then The text description of the requirement should be pasted with the HTML formatting intact

Feature: Managing Requirements in ReqView Application

Scenario: Permanently remove selected deleted requirements or document sections
Given user is logged into ReqView application
When user selects a deleted requirement or document section
And user clicks on the "Permanently Remove" button
Then that requirement or document section should be permanently removed from the document.

Scenario: Editing the heading of the selected section
Given user is logged into ReqView application
When user selects a section
And edits the heading of the selected section
Then the heading should be updated in the document.

Scenario: Editing the text description of the selected requirement
Given user is logged into ReqView application
When user selects a requirement
And edits the text description of the selected requirement
Then the text description should be updated in the document.

Scenario: Pasting HTML content from other applications into requirement text description
Given user is logged into ReqView application
When user selects a requirement
And pastes an HTML content from other applications into the text description
Then the HTML content should be successfully pasted in the document.

Scenario: Defining custom requirement attributes and assigning unique ID
Given user is logged into ReqView application
When user selects the "Custom Attributes" option
And defines a new custom attribute with a unique ID
Then the custom attribute should be added to the list of attributes.

Scenario: Changing type of custom attribute
Given user is logged into ReqView application
When user selects a custom attribute
And changes the type
Then all values of that attribute should be automatically converted to the new type.

Scenario: Automatic conversion fails for custom attribute value
Given user is logged into ReqView application
When user changes the type of a custom attribute
And the automatic conversion fails for any attribute value
Then the application should prevent the change of custom attribute type.

Scenario: Setting an optional name for custom attribute
Given user is logged into ReqView application
When user selects a custom attribute
And sets an optional name
Then that name should be displayed in the list of attributes.

Scenario: Removing custom attributes
Given user is logged into ReqView application
When user selects a custom attribute
And clicks on the "Remove" button
Then the attribute should be removed from the list of attributes.

Scenario: Unsetting values of removed custom attribute in all requirements
Given user is logged into ReqView application
When user removes a custom attribute
Then the values of that attribute should be unset in all requirements.

Scenario: Editing custom attributes of the selected requirement
Given user is logged into ReqView application
When user selects a requirement
And edits the custom attributes
Then the changes should be reflected in the document.

Scenario: Attaching images or documents to the selected requirement
Given user is logged into ReqView application
When user selects a requirement
And clicks on the "Attach" button
And attaches one or more images or documents
Then those attachments should be added to the document.

Scenario: Generating unique attachment ID for new attachments
Given user is logged into ReqView application
When user attaches a new file to the document
Then a unique attachment ID should be generated for that attachment.

Scenario: Saving attachments to local file system
Given user is logged into ReqView application
When user selects an attachment
And clicks on the "Save" button
Then the attachment should be saved to the local file system.

Scenario: Updating content of requirement attachments from selected file
Given user is logged into ReqView application
When user selects an attachment
And clicks on the "Update" button
And selects a file
Then the content of the attachment should be updated with the content of the selected file.

Scenario: Permanently removing attachments from the document
Given user is logged into ReqView application
When user selects an attachment
And clicks on the "Remove" button
Then that attachment should be permanently removed from the document.

Scenario: Commenting on the selected requirement
Given user is logged into ReqView application
When user selects a requirement
And clicks on the "Comment" button
And adds a comment
Then the comment should be added to the requirement with current date, time and author.

Scenario: Defining link types and assigning unique ID
Given user is logged into ReqView application
When user selects the "Traceability Links Configuration" option
And defines a new link type with a unique ID
Then the new link type should be added to the list of link types.

Scenario: Setting name and role for link type
Given user is logged into ReqView application
When user selects a link type
And sets a name and role for that link type
Then those values should be saved for that link type.

Scenario: Removing link type
Given user is logged into ReqView application
When user selects a link type
And clicks on the "Remove" button
Then that link type should be removed from the list of link types.

Scenario: Removing all traceability links of a link type
Given user is logged into ReqView application
When user removes a link type
Then all traceability links of that link type should be removed from the document.

Scenario: Creating directed traceability links between requirements
Given user is logged into ReqView application
When user selects two requirements
And clicks on the "Create Traceability Link" button
And selects a link type
Then a directed traceability link should be created between those requirements with the selected link type.

Scenario: Changing the link type of a selected traceability link
Given user is logged into ReqView application
When user selects a traceability link
And changes the link type
Then that link should be updated with the new link type.

Scenario: Reverting direction of a selected traceability link
Given user is logged into ReqView application
When user selects a traceability link
And clicks on the "Revert Direction" button
Then the direction of that link should be reversed.

Scenario: Negative testing for invalid input
Given user is logged into ReqView application
When user enters invalid input
Then the application should display an error message.

Scenario: Performance testing for large document
Given user is logged into ReqView application
When the document size exceeds a certain threshold
And user performs various operations such as creating, editing, deleting requirements and attachments
Then the application should perform optimally without any delay or errors.

(Note: This is a sample feature file for demonstration purposes only. Tests should be written according to specific project requirements and guidelines.)


Feature: Traceability Links Configuration
  As a user of the application
  I want to be able to manage and configure traceability links
  So that I can properly track and document the relationships between requirements

Scenario: Define and Assign Unique ID to Link Types
  Given I am on the Traceability Links Configuration page
  When I create a new link type with a unique ID
  Then the link type is successfully saved and cannot be changed

Scenario: Set Name and Role for Link Type
  Given I am on the Traceability Links Configuration page
  When I select a link type
  And I set its name and role for both source and target requirements
  Then the changes are successfully saved

Scenario: Remove Link Type
  Given I am on the Traceability Links Configuration page
  When I select a link type
  And I click on the remove button
  Then the link type is removed from the list

Scenario: Remove Link Type and Its Traceability Links
  Given I am on the Traceability Links Configuration page
  When I select a link type
  And I click on the remove button
  Then all traceability links of the link type are also removed from the document

Feature: Traceability Links
  As a user of the application
  I want to be able to create, modify, and remove traceability links
  So that I can easily track and manage the relationships between requirements

Scenario: Create Directed Traceability Links
  Given I am on the Traceability Links page
  And I have selected a link type
  When I choose two requirements or document sections to create a traceability link between
  Then a directed traceability link of the chosen type is created

Scenario: Change Link Type of Selected Traceability Link
  Given I am on the Traceability Links page
  And I have selected a traceability link
  When I change the link type
  Then the traceability link is updated with the new type

Scenario: Revert Direction of Selected Traceability Link
  Given I am on the Traceability Links page 
  And I have selected a traceability link
  When I click on the revert button
  Then the direction of the traceability link is reversed

Scenario: Permanently Remove Traceability Link
  Given I am on the Traceability Links page
  And I have selected a traceability link
  When I click on the remove button
  Then the traceability link is permanently removed from the document

Feature: Auto Save
  As a user of the application
  I want the document to automatically save my changes
  So that I do not have to manually save or risk losing my work

Scenario: Persist and Restore Document Changes 
  Given I have made changes to the document  
  And I close and restart the application  
  Then my changes are successfully restored  

Scenario: Clear Persisted Document Data 
  Given I have made changes to the document  
  And I close the document  
  And I reopen the document  
  Then all persisted data is cleared  

Feature: Filtering
  As a user of the application
  I want to be able to filter requirements based on specific criteria
  So that I can easily find and view the requirements I need

Scenario: Filter Requirements According to DNF Condition
  Given I am on the Filtering page
  When I enter a condition in disjunctive normal form (DNF)
  Then the requirements are filtered according to the condition

Scenario: Filter Requirements by Document Sections
  Given I am on the Filtering page
  When I enter a condition that matches document sections by number or heading
  Then the requirements associated with those sections are filtered

Scenario: Filter Requirements by Description or Custom Attribute
  Given I am on the Filtering page
  When I enter a condition that matches requirements by text description or a custom attribute
  Then the requirements are filtered by the specified criteria

Scenario: Filter Requirements with Missing Traceability Links
  Given I am on the Filtering page
  When I select a link type
  And I enter a condition to filter requirements with missing links of that type
  Then the requirements are filtered accordingly

Feature: Full Text Search
  As a user of the application
  I want to be able to search for requirements using keywords
  So that I can quickly find specific requirements

Scenario: Search for Requirements by Keywords
  Given I am on the Full Text Search page
  When I enter one or more keywords in the search bar
  Then the requirements containing those keywords in their string or xhtml attributes are highlighted

Scenario: Select Next or Previous Matched Requirement
  Given I am on the Full Text Search page
  And I have entered keywords in the search bar
  When I click on the next or previous button
  Then the next or previous matched requirement is selected and highlighted

Feature: History of Changes
  As a user of the application
  I want to be able to view the history of changes for a requirement
  So that I can track and see who has made modifications to the requirement

Scenario: Record Date, Time, and Author of Requirement Change
  Given I have made changes to a requirement
  Then the current date and time and my name are recorded as the author of the change

Scenario: Display Changes of Selected Requirement
  Given I am viewing a requirement
  When I click on the History pane
  Then all recorded changes for the selected requirement are displayed in chronological order

Scenario: Expand and Collapse Changes in History Pane
  Given I am viewing a requirement's History pane
  When I click on the expand or collapse button
  Then the changes for that requirement are either expanded or collapsed in the view

Feature: Reporting
  As a user of the application
  I want to be able to print or create a PDF of the displayed requirements table
  So that I can easily share or save the information for future use

Scenario: Print Displayed Requirements Table
  Given I am on the Reporting page
  When I click on the print button 
  Then the displayed requirements table is sent to the default printer

Scenario: Create PDF of Displayed Requirements Table
  Given I am on the Reporting page
  When I click on the create PDF button
  Then a PDF containing the displayed requirements table is created and saved.

