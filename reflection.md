# PawPal+ Project Reflection

## 1. System Design

**a. Core user actions (natural language)**

- A user can add and manage their pet profile, including basic details and care preferences.
- A user can create and update care tasks (like feeding, walks, medication, and play) with duration and priority.
- A user can generate and review today's care plan so they know what to do and when.

**b. Initial design**

-   **`Pet`**: This class was designed to hold all information about a pet, such as its name, species, and any special needs or preferences.
-   **`Activity`**: This class represented a task that needed to be scheduled, like 'walk', 'feed', or 'play'. Each activity had a `duration` and a `priority` level (e.g., high, medium, low).
-   **`Scheduler`**: This was the main engine of the system. Its responsibility was to take a list of pets and their required activities for a day and generate a conflict-free schedule. The initial plan was for it to simply order activities by priority.
-   **`Schedule`**: A simple data structure class, intended to hold the final output: an ordered list of `Activity` objects, each assigned a specific start time.

**c. Design changes**
Yes, my design evolved significantly once I started implementing the scheduling logic.

One key change was the enhancement of the `Activity` class. Initially, I only had a `priority` attribute to guide the scheduler. I quickly realized this was insufficient. For example, giving a dog its medication is a high-priority task, but it also needs to happen at a very specific time. A 'play' session might be lower priority but is flexible about when it happens.

To address this, I added the concept of a time window to the `Activity` class by including `earliest_start_time` and `latest_start_time` attributes. This allowed me to represent both fixed appointments and flexible tasks within the same structure. This change was crucial because it made the `Scheduler`'s job more explicit. Instead of just relying on a simple priority score, the scheduler could now operate on concrete time constraints, making the scheduling algorithm more powerful and the resulting schedules far more practical and realistic. It separated the definition of an activity's constraints from the scheduling algorithm itself.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
