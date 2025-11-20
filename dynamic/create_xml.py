from gviz import svg_to_data_uri

def int_to_char(start, i):
    return chr(ord(start) + i)


def escape_html(s):
    # IMPORTANT: Escape ampersand first to avoid double-escaping
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")


def format_list(l):
    return "list(" + ",".join(l) + ")"

def format_variable_declaration(name, id, code):
    return """
    <VariableDeclaration id="{id1}">
      <name>{name}</name>
      <initializationCode id="{id2}">
        <code>{code}</code>
        <domain>MATH</domain>
      </initializationCode>
    </VariableDeclaration>
    """.format(id1=id, id2=id + 1, name=name, code=escape_html(code))

def format_graphviz_graph(graph):
    svg = graph.pipe(format='svg').decode('utf-8')
    svg = "\"<img src=" + svg_to_data_uri(svg[svg.index('<svg'):]) + ">\""
    return svg

def format_graphviz_graphs(name, id, graphs):
    return format_variable_declaration(name, id, format_list([format_graphviz_graph(graph) for graph in graphs]))

def format_solutions(solutions):
    return format_list(
        [format_list(
            ["'" + item + "'" for item in solution]
        ) for solution in solutions]
    )

def format_all_solutions(name, id, all_solutions):
    return format_variable_declaration(name, id, format_list([format_solutions(solutions) for solutions in all_solutions]))

def node_to_edge_solutions(solutions, edges):
    return [list(edges).index(edge) for edge in zip(solutions[0:-1], solutions[1:])]


def format_draggable(name, id):
    return f'''<DNDVisibleZonesDraggable id="{id}">
    <variableName>{name}</variableName>
    <htmlContent>&lt;div&gt;{name}&lt;/div&gt;</htmlContent>
    <numberOfDraggables>1</numberOfDraggables>
    <infiniteDraggables>false</infiniteDraggables>
    <dndVisibleZonesStage reference="5"/>
</DNDVisibleZonesDraggable>
'''

def format_draggables(start, id , num):
    string = ""
    for i in range(num):
        string += format_draggable(int_to_char(start, i), id)
        id += 1
    return string


def format_mc_answer(answer_text, id, order, is_correct=False):
    """Format a single multiple choice answer option"""
    rule = "CORRECT" if is_correct else "WRONG"
    return f'''<MCAnswer id="{id}">
              <order>{order}</order>
              <rule>{rule}</rule>
              <text>&lt;div&gt;{escape_html(answer_text)}&lt;/div&gt;</text>
              <variableName></variableName>
              <mcstage reference="5"/>
            </MCAnswer>
'''


def format_mc_answers(answers, start_id):
    """Format multiple choice answers from a list of tuples (text, is_correct)
    Returns tuple of (xml_string, next_id, correct_indices)
    """
    xml = ""
    correct_indices = []
    for i, (answer_text, is_correct) in enumerate(answers):
        xml += format_mc_answer(answer_text, start_id + i, i, is_correct)
        if is_correct:
            correct_indices.append(i + 1)  # IDs start at start_id
    return xml, start_id + len(answers), correct_indices


def format_mc_stage(task_description, answers, all_solutions_html, start_id, stage_id=5):
    """Format a complete MCStage for multiple choice questions with dynamic feedback
    
    Args:
        task_description: HTML description of the question
        answers: List of tuples [(answer_text, is_correct), ...]
        all_solutions_html: Pre-formatted HTML string of all valid solutions
        start_id: Starting ID for XML elements
        stage_id: Reference ID for the stage
    
    Returns:
        Tuple of (XML string for the MC stage, next_id)
    """
    answers_xml, next_id, correct_indices = format_mc_answers(answers, start_id)
    
    # Create dynamic feedback with solution
    correct_ids_str = ",".join([str(idx) for idx in correct_indices])
    
    return f'''<MCStage id="{stage_id}">
      <internalName>#1</internalName>
      <externalName>Subtask 1</externalName>
      <taskDescription>&lt;div&gt;[var=graph]&lt;/div&gt;
&lt;div&gt;{escape_html(task_description)}&lt;/div&gt;
        </taskDescription>
      <feedbackRules id="{start_id + 100}">
        <FeedbackRule id="{start_id + 101}">
          <name>Correct Answer</name>
          <orderIndex>0</orderIndex>
          <validationExpression id="{start_id + 102}">
            <code>evaluateInR("any(getAnswerIdsForSelectedAnswers([input=dropArea1]) %in% c({correct_ids_str}))")</code>
            <domain>MATH</domain>
          </validationExpression>
          <feedbackText>&lt;div&gt;&lt;strong&gt;Correct.&lt;/strong&gt;&lt;/div&gt;&lt;div&gt;&lt;br/&gt;Solution:&lt;br/&gt;&lt;br/&gt;[var=feedback_solutions]&lt;/div&gt;</feedbackText>
          <points>1</points>
          <terminal>true</terminal>
          <fieldsToBeMarked id="{start_id + 103}"/>
        </FeedbackRule>
        <FeedbackRule id="{start_id + 104}">
          <name>Incorrect Answer</name>
          <orderIndex>1</orderIndex>
          <validationExpression id="{start_id + 105}">
            <code>1</code>
            <domain>MATH</domain>
          </validationExpression>
          <feedbackText>&lt;div&gt;&lt;strong&gt;Incorrect.&lt;/strong&gt;&lt;/div&gt;&lt;div&gt;&lt;br/&gt;Solution:&lt;br/&gt;&lt;br/&gt;[var=feedback_solutions]&lt;/div&gt;</feedbackText>
          <points>0</points>
          <terminal>false</terminal>
          <fieldsToBeMarked id="{start_id + 106}"/>
        </FeedbackRule>
      </feedbackRules>
      <defaultTransition id="{start_id + 107}">
        <conditionExpression id="{start_id + 108}">
          <domain>MATH</domain>
        </conditionExpression>
        <stageExpression id="{start_id + 109}">
          <domain>MATH</domain>
        </stageExpression>
        <type>NEXT_OR_END</type>
        <extraWeight>0</extraWeight>
      </defaultTransition>
      <skipTransitions id="{start_id + 110}"/>
      <stageTransitions id="{start_id + 111}"/>
      <hints id="{start_id + 112}"/>
      <variableUpdatesOnEnter id="{start_id + 113}"/>
      <variableUpdatesBeforeCheck id="{start_id + 114}"/>
      <variableUpdatesAfterCheck id="{start_id + 115}"/>
      <variableUpdatesOnNormalExit id="{start_id + 116}"/>
      <variableUpdatesOnRepeat id="{start_id + 117}"/>
      <variableUpdatesOnSkip id="{start_id + 118}"/>
      <weight>1</weight>
      <orderIndex>0</orderIndex>
      <allowSkip>false</allowSkip>
      <resources id="{start_id + 119}"/>
      <answerOptions id="{start_id + 120}">
        {answers_xml}
      </answerOptions>
      <randomize>true</randomize>
      <correctAnswerFeedback>&lt;div&gt;&lt;strong&gt;Correct.&lt;/strong&gt;&lt;/div&gt;&lt;div&gt;&lt;br/&gt;Solution:&lt;br/&gt;&lt;br/&gt;[var=feedback_solutions]&lt;/div&gt;</correctAnswerFeedback>
      <pointMode>MANUAL</pointMode>
      <feedbackDisplayMode>FIRST</feedbackDisplayMode>
      <defaultFeedback>&lt;div&gt;&lt;strong&gt;Incorrect.&lt;/strong&gt;&lt;/div&gt;&lt;div&gt;&lt;br/&gt;Solution:&lt;br/&gt;&lt;br/&gt;[var=feedback_solutions]&lt;/div&gt;</defaultFeedback>
      <defaultResult>0</defaultResult>
      <extraFeedbacks id="{start_id + 121}"/>
    </MCStage>
''', next_id


def format_mc_stage_dynamic(task_description, num_answers, start_id, stage_id=5):
    """Format a complete MCStage with dynamic answer options from variable
    
    Args:
        task_description: HTML description of the question (generic, will be same for all)
        num_answers: Number of answer options (for reference)
        start_id: Starting ID for XML elements
        stage_id: Reference ID for the stage
    
    Returns:
        Tuple of (XML string for the MC stage, next_id)
    """
    # Generate answer options referencing answer_text_1, answer_text_2, etc.
    answers_xml = ""
    for i in range(num_answers):
        rule = "CORRECT" if i == 0 else "WRONG"  # first answer constructed as correct
        answers_xml += f'''<MCAnswer id="{start_id + i}">
              <order>{i}</order>
              <rule>{rule}</rule>
              <text>&lt;div&gt;[var=answer_text_{i+1}]&lt;/div&gt;</text>
              <variableName></variableName>
              <mcstage reference="5"/>
            </MCAnswer>
'''
    
    # Generate R expressions for checking if each answer index is selected AND correct
    # Build validation expression that checks if any selected answer is in correct_answer_indices
    validation_code = "any(c("
    for i in range(num_answers):
        # Each term: if mcindex_i is selected AND i (0-based) is in correct_answer_indices
        validation_code += f"([input=mcindex_{i}] & ({i} %in% [var=correct_answer_indices]))"
        if i < num_answers - 1:
            validation_code += ", "
    validation_code += "))"
    
    return f'''<MCStage id="{stage_id}">
      <internalName>#1</internalName>
      <externalName>Subtask 1</externalName>
      <taskDescription>&lt;div&gt;[var=graph]&lt;/div&gt;
&lt;div&gt;Which of the following is a valid Hamiltonian path in this graph starting from node [var=start_node]?&lt;/div&gt;
        </taskDescription>
      <feedbackRules id="{start_id + 100}">
        <FeedbackRule id="{start_id + 101}">
          <name>Correct Answer</name>
          <orderIndex>0</orderIndex>
          <validationExpression id="{start_id + 102}">
            <code>{escape_html(validation_code)}</code>
            <domain>MATH</domain>
          </validationExpression>
          <feedbackText>&lt;div&gt;&lt;strong&gt;Correct.&lt;/strong&gt;&lt;/div&gt;&lt;div&gt;&lt;br/&gt;Solution:&lt;br/&gt;&lt;br/&gt;[var=feedback_solutions]&lt;/div&gt;</feedbackText>
          <points>1</points>
          <terminal>true</terminal>
          <fieldsToBeMarked id="{start_id + 103}"/>
        </FeedbackRule>
        <FeedbackRule id="{start_id + 104}">
          <name>Incorrect Answer</name>
          <orderIndex>1</orderIndex>
          <validationExpression id="{start_id + 105}">
            <code>TRUE</code>
            <domain>MATH</domain>
          </validationExpression>
          <feedbackText>&lt;div&gt;&lt;strong&gt;Incorrect.&lt;/strong&gt;&lt;/div&gt;&lt;div&gt;&lt;br/&gt;Solution:&lt;br/&gt;&lt;br/&gt;[var=feedback_solutions]&lt;/div&gt;</feedbackText>
          <points>0</points>
          <terminal>false</terminal>
          <fieldsToBeMarked id="{start_id + 106}"/>
        </FeedbackRule>
      </feedbackRules>
      <defaultTransition id="{start_id + 107}">
        <conditionExpression id="{start_id + 108}">
          <domain>MATH</domain>
        </conditionExpression>
        <stageExpression id="{start_id + 109}">
          <domain>MATH</domain>
        </stageExpression>
        <type>NEXT_OR_END</type>
        <extraWeight>0</extraWeight>
      </defaultTransition>
      <skipTransitions id="{start_id + 110}"/>
      <stageTransitions id="{start_id + 111}"/>
      <hints id="{start_id + 112}"/>
      <variableUpdatesOnEnter id="{start_id + 113}"/>
      <variableUpdatesBeforeCheck id="{start_id + 114}"/>
      <variableUpdatesAfterCheck id="{start_id + 115}"/>
      <variableUpdatesOnNormalExit id="{start_id + 116}"/>
      <variableUpdatesOnRepeat id="{start_id + 117}"/>
      <variableUpdatesOnSkip id="{start_id + 118}"/>
      <weight>1</weight>
      <orderIndex>0</orderIndex>
      <allowSkip>false</allowSkip>
      <resources id="{start_id + 119}"/>
      <answerOptions id="{start_id + 120}">
        {answers_xml}
      </answerOptions>
      <randomize>true</randomize>
      <correctAnswerFeedback>&lt;div&gt;&lt;strong&gt;Correct.&lt;/strong&gt;&lt;/div&gt;&lt;div&gt;&lt;br/&gt;Solution:&lt;br/&gt;&lt;br/&gt;[var=feedback_solutions]&lt;/div&gt;</correctAnswerFeedback>
      <pointMode>MANUAL</pointMode>
      <feedbackDisplayMode>FIRST</feedbackDisplayMode>
      <defaultFeedback>&lt;div&gt;&lt;strong&gt;Incorrect.&lt;/strong&gt;&lt;/div&gt;&lt;div&gt;&lt;br/&gt;Solution:&lt;br/&gt;&lt;br/&gt;[var=feedback_solutions]&lt;/div&gt;</defaultFeedback>
      <defaultResult>0</defaultResult>
      <extraFeedbacks id="{start_id + 121}"/>
    </MCStage>
''', start_id + num_answers + 122


def format_mc_stage_dynamic_tf(question_text, num_answers, start_id, stage_id=5):
    """Format a True/False MCStage for Hamiltonian cycle existence (English).

    Assumes variables:
      - graph
      - feedback_cycles (HTML list of cycles or 'No Hamiltonian cycle')
      - correct_answer_indices (list of zero-based correct indices)
      - answer_text_1 .. answer_text_num_answers
    """
    # Build answers (first answer always marked CORRECT; ordering handled upstream)
    answers_xml = ""
    for i in range(num_answers):
        rule = "CORRECT" if i == 0 else "WRONG"
        answers_xml += f'''<MCAnswer id="{start_id + i}">
              <order>{i}</order>
              <rule>{rule}</rule>
              <text>&lt;div&gt;[var=answer_text_{i+1}]&lt;/div&gt;</text>
              <variableName></variableName>
              <mcstage reference="{stage_id}"/>
            </MCAnswer>
'''

    # Validation expression: any selected index is in correct_answer_indices
    validation_code = "any(c(" + ", ".join(
        f"([input=mcindex_{i}] & ({i} %in% [var=correct_answer_indices]))" for i in range(num_answers)
    ) + "))"

    return f'''<MCStage id="{stage_id}">
      <internalName>#1</internalName>
      <externalName>Subtask 1</externalName>
      <taskDescription>&lt;div&gt;[var=graph]&lt;/div&gt;
&lt;div&gt;{escape_html(question_text)}&lt;/div&gt;
        </taskDescription>
      <feedbackRules id="{start_id + 100}">
        <FeedbackRule id="{start_id + 101}">
          <name>Correct answer</name>
          <orderIndex>0</orderIndex>
          <validationExpression id="{start_id + 102}">
            <code>{escape_html(validation_code)}</code>
            <domain>MATH</domain>
          </validationExpression>
          <feedbackText>&lt;div&gt;&lt;strong&gt;Correct.&lt;/strong&gt;&lt;/div&gt;&lt;div&gt;&lt;br/&gt;Hamiltonian cycle(s):&lt;br/&gt;&lt;br/&gt;[var=feedback_cycles]&lt;/div&gt;</feedbackText>
          <points>1</points>
          <terminal>true</terminal>
          <fieldsToBeMarked id="{start_id + 103}"/>
        </FeedbackRule>
        <FeedbackRule id="{start_id + 104}">
          <name>Incorrect answer</name>
          <orderIndex>1</orderIndex>
          <validationExpression id="{start_id + 105}">
            <code>TRUE</code>
            <domain>MATH</domain>
          </validationExpression>
          <feedbackText>&lt;div&gt;&lt;strong&gt;Incorrect.&lt;/strong&gt;&lt;/div&gt;&lt;div&gt;&lt;br/&gt;Hamiltonian cycle(s):&lt;br/&gt;&lt;br/&gt;[var=feedback_cycles]&lt;/div&gt;</feedbackText>
          <points>0</points>
          <terminal>false</terminal>
          <fieldsToBeMarked id="{start_id + 106}"/>
        </FeedbackRule>
      </feedbackRules>
      <defaultTransition id="{start_id + 107}">
        <conditionExpression id="{start_id + 108}">
          <domain>MATH</domain>
        </conditionExpression>
        <stageExpression id="{start_id + 109}">
          <domain>MATH</domain>
        </stageExpression>
        <type>NEXT_OR_END</type>
        <extraWeight>0</extraWeight>
      </defaultTransition>
      <skipTransitions id="{start_id + 110}"/>
      <stageTransitions id="{start_id + 111}"/>
      <hints id="{start_id + 112}"/>
      <variableUpdatesOnEnter id="{start_id + 113}"/>
      <variableUpdatesBeforeCheck id="{start_id + 114}"/>
      <variableUpdatesAfterCheck id="{start_id + 115}"/>
      <variableUpdatesOnNormalExit id="{start_id + 116}"/>
      <variableUpdatesOnRepeat id="{start_id + 117}"/>
      <variableUpdatesOnSkip id="{start_id + 118}"/>
      <weight>1</weight>
      <orderIndex>0</orderIndex>
      <allowSkip>false</allowSkip>
      <resources id="{start_id + 119}"/>
      <answerOptions id="{start_id + 120}">
        {answers_xml}
      </answerOptions>
      <randomize>true</randomize>
      <correctAnswerFeedback>&lt;div&gt;&lt;strong&gt;Correct.&lt;/strong&gt;&lt;/div&gt;&lt;div&gt;&lt;br/&gt;Hamiltonian cycle(s):&lt;br/&gt;&lt;br/&gt;[var=feedback_cycles]&lt;/div&gt;</correctAnswerFeedback>
      <pointMode>MANUAL</pointMode>
      <feedbackDisplayMode>FIRST</feedbackDisplayMode>
      <defaultFeedback>&lt;div&gt;&lt;strong&gt;Incorrect.&lt;/strong&gt;&lt;/div&gt;&lt;div&gt;&lt;br/&gt;Hamiltonian cycle(s):&lt;br/&gt;&lt;br/&gt;[var=feedback_cycles]&lt;/div&gt;</defaultFeedback>
      <defaultResult>0</defaultResult>
      <extraFeedbacks id="{start_id + 121}"/>
    </MCStage>
''', start_id + num_answers + 122



